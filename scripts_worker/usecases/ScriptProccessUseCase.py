import json
import logging
import sys
from asyncio import sleep
from dataclasses import dataclass, field
from random import randint
from typing import Optional

from aio_pika import IncomingMessage
from telethon.errors import (ChatWriteForbiddenError, SlowModeWaitError, ChatRestrictedError, ChannelPrivateError,
                             ForbiddenError, ChatAdminRequiredError, ChatGuestSendForbiddenError, PhoneNumberBannedError,
                             UserBannedInChannelError)

from abstractions.usecases.CampaignsUseCaseInterface import CampaignsUseCaseInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from abstractions.usecases.TemplateEngineInterface import TemplateEngineInterface
from abstractions.usecases.WorkersUseCaseInterface import WorkersUseCaseInterface
from abstractions.usecases.watcher import WatcherInterface
from domain.events.scripts import NewActiveScript
from domain.models import ScriptForCampaign as ScriptForCampaignModel, ChatProcess, MessageProcess
from domain.reports import SetTargetChatsRequest, SetMessageStatusRequest, SetChatStatusRequest, SetScriptStatusRequest
from usecases.exceptions import NoSuchCampaignError, NoSuchScriptError

logger = logging.getLogger(__name__)


@dataclass
class ScriptProcessUseCase:
    scripts_use_case: ScriptsUseCaseInterface
    workers_use_case: WorkersUseCaseInterface
    campaign_use_case: CampaignsUseCaseInterface

    template_engine: TemplateEngineInterface

    watcher: WatcherInterface

    process_id: str = ''
    process: list[ChatProcess] = field(default_factory=list)

    async def activate_new_script(self, event: NewActiveScript):
        logger.info(f"New script activating request received: {event}")

        sfc = await self.scripts_use_case.get_active_script(sfc_id=event.script_for_campaign_id)

        if sfc.done:
            logger.error(f"SFC {sfc.id} is done, skipping")
            return

        await self.process_script(sfc)

    async def _get_campaign_delay(self, campaign_id: str) -> tuple[int, int]:
        campaign = await self.campaign_use_case.get_campaign(campaign_id)
        delay_from, delay_to = map(int, campaign.chat_answer_wait_interval_seconds.split("-"))
        return delay_from, delay_to

    async def _get_target_chats(self, sfc: ScriptForCampaignModel) -> list[Optional[str]]:  # TODO: Annotated
        bots = [await self.workers_use_case.get_by_username(value) for key, value in sfc.bots_mapping.items()]
        res = []
        for bot in bots:
            if not bot.chats:
                continue

            res.extend(bot.chats)
        target_chats = list(set(res))
        return target_chats

    async def process_script(self, sfc: ScriptForCampaignModel):
        logger.info(f"Processing script {sfc.id}")
        script_id, campaign_id = sfc.script_id, sfc.campaign_id  # TODO: refactor?

        campaign = await self.campaign_use_case.get_campaign(campaign_id)
        if not campaign:
            raise NoSuchCampaignError(f'There is no campaign with id "{campaign_id}"')

        script = await self.scripts_use_case.get_script(script_id)
        if not script:
            raise NoSuchScriptError(f'There is no script with id "{script_id}"')

        self.process_id = await self.watcher.report_new_activation(sfc_id=sfc.id)

        target_chats = await self._get_target_chats(sfc)
        logger.info(f"Target chats: {target_chats}")

        process = await self.watcher.report_target_chats(  # TODO: refactor to method
            report=SetTargetChatsRequest(
                process_id=self.process_id,
                target_chats=target_chats,
            )
        )
        self.process = process

        successful_processed = True

        for chat in target_chats:
            if not chat:
                continue

            logger.info(f"Working with chat {chat}")
            messages = await self.scripts_use_case.start_script(script_id)
            bots_mapping = sfc.bots_mapping
            bots_mapping = {key: await self.workers_use_case.get(value) for key, value in bots_mapping.items()}

            last_message_id: Optional[int] = None
            writable = True
            reason_of_fail = None
            for message in messages:
                delay = await self._get_random_sleep(campaign.id)
                logger.info(f"delay: {delay}")
                await sleep(delay)

                # if stopped by admin
                if await self.scripts_use_case.get_sfc_stop_status(sfc_id=sfc.id):
                    logger.info(f"Active script {sfc.id} was stopped (script template {sfc.script_id})")
                    return

                logger.info(message.text)
                text_to_send = await self.template_engine.process_template(message.text)
                worker_id = bots_mapping[str(message.bot_index)].id  # TODO: resolve fucking types
                try:
                    new_message_id = await self.workers_use_case.send_message(
                        chat_id=chat,
                        bot_id=worker_id,
                        message=text_to_send,
                        reply_to=last_message_id,
                    )
                    last_message_id = new_message_id
                except Exception as e:
                    logger.error(
                        f"There is an error sending message {text_to_send} from bot {worker_id} to {chat}: {type(e).__name__}: {e}",
                        exc_info=True
                    )
                    writable = False
                    reason_of_fail = e
                    successful_processed = False
                    await self.report_failed_message(
                        chat_link=chat,
                        bot_id=worker_id,
                        unprocessed_text=message.text,
                    )
                    break
                else:
                    await self.report_successful_message(
                        chat_link=chat,
                        bot_id=worker_id,
                        unprocessed_text=message.text,
                        processed_text=text_to_send,
                    )
            if writable:
                logger.info(f"All messages from script {script_id} are sent to chat {chat}")
                await self.report_successful_chat(chat_link=chat)
            else:
                logger.info(f"Skipped chat {chat}")
                if isinstance(reason_of_fail, ChatWriteForbiddenError) or isinstance(reason_of_fail, ForbiddenError):
                    reason = 'Нельзя писать в чат'
                elif isinstance(reason_of_fail, ValueError) and chat.split('/')[-1].isdigit():
                    reason = 'Некорректная ссылка на чат'
                elif isinstance(reason_of_fail, ChannelPrivateError):
                    reason = "Приватный чат, в который бот не добавлен, либо бан"
                elif isinstance(reason_of_fail, ChatAdminRequiredError):
                    reason = 'Запрещенные слова, ссылка устарела или несуществующий чат'
                elif isinstance(reason_of_fail, ChatGuestSendForbiddenError):
                    reason = 'Бот не добавлен в чат (чат является дискуссионным, т.е. для комментариев в канале)'
                elif isinstance(reason_of_fail, SlowModeWaitError):
                    reason = 'В чате включен медленный режим'
                elif isinstance(reason_of_fail, PhoneNumberBannedError):
                    reason = ('Номер телефона забанен в Telegram. '
                              'Если это первый бан для аккаунта, его снимут через несколько дней.')
                elif isinstance(reason_of_fail, UserBannedInChannelError):
                    reason = 'Этот аккаунт не может отправлять сообщения в группы/каналы'
                else:
                    reason = f'Неизвестная ошибка ({type(reason_of_fail)})'
                await self.report_failed_chat(
                    chat_link=chat,
                    on_message=message.text,
                    reason=reason,
                )

        logger.info(f"All messages from script {script_id} are sent to all chats")
        await self._report_script(success=successful_processed)

        await self.scripts_use_case.sfc_done(sfc.id)

    async def _get_random_sleep(self, campaign_id: str):
        delays = await self._get_campaign_delay(campaign_id)
        return randint(delays[0], delays[1])

    async def _get_message_id(self, chat_link: str, bot_id: str, unprocessed_text: str) -> str:
        if not self.process:
            raise RuntimeError('Process is not retrieved yet')

        chat: ChatProcess = tuple(filter(
            lambda x: x.chat_link == chat_link,
            self.process
        ))[0]

        message: MessageProcess = tuple(filter(
            lambda x: x.bot_id == bot_id and x.text == unprocessed_text,
            chat.messages
        ))[0]

        return message.id

    async def report_successful_message(
            self,
            chat_link: str,
            bot_id: str,
            unprocessed_text: str,
            processed_text: str,
    ) -> None:
        message_id = await self._get_message_id(
            chat_link=chat_link,
            bot_id=bot_id,
            unprocessed_text=unprocessed_text,
        )

        report = SetMessageStatusRequest(
            process_id=self.process_id,
            message_id=message_id,
            is_sent=True,
            text=processed_text,
        )

        await self.watcher.report_message_status(
            report=report,
        )

    async def report_failed_message(self, chat_link: str, bot_id: str, unprocessed_text: str):
        message_id = await self._get_message_id(
            chat_link=chat_link,
            bot_id=bot_id,
            unprocessed_text=unprocessed_text,
        )

        report = SetMessageStatusRequest(
            process_id=self.process_id,
            message_id=message_id,
            is_sent=False,
        )

        await self.watcher.report_message_status(
            report=report,
        )

    async def report_successful_chat(self, chat_link: str):
        await self._report_chat(chat_link=chat_link, successful=True)

    async def report_failed_chat(self, chat_link: str, on_message: str, reason: str):
        await self._report_chat(chat_link=chat_link, successful=False, on_message=on_message, reason=reason)

    async def _report_chat(self, chat_link: str, successful: bool, on_message: str = None, reason: str = None):
        report = SetChatStatusRequest(
            process_id=self.process_id,
            chat_link=chat_link,
            is_successful=successful,
            on_message=on_message,
            reason=reason,
        )

        await self.watcher.report_chat_status(
            report=report,
        )

    async def _report_script(self, success: bool):
        report = SetScriptStatusRequest(
            process_id=self.process_id,
            is_successful=success,
        )

        await self.watcher.report_script_status(
            report=report
        )
