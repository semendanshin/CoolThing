import json
import logging
from asyncio import sleep
from dataclasses import dataclass
from random import randint
from typing import Optional

from aio_pika import IncomingMessage

from abstractions.usecases.CampaignsUseCaseInterface import CampaignsUseCaseInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from abstractions.usecases.TemplateEngineInterface import TemplateEngineInterface
from abstractions.usecases.WorkersUseCaseInterface import WorkersUseCaseInterface
from domain.events.scripts import NewActiveScript
from domain.models import ScriptForCampaign as ScriptForCampaignModel
from usecases.exceptions import NoSuchCampaignError, NoSuchScriptError

logger = logging.getLogger(__name__)


@dataclass
class ScriptProcessUseCase:
    scripts_use_case: ScriptsUseCaseInterface
    workers_use_case: WorkersUseCaseInterface
    campaign_use_case: CampaignsUseCaseInterface

    template_engine: TemplateEngineInterface

    async def activate_new_script(self, message: IncomingMessage):
        event = NewActiveScript(**json.loads(message.body.decode()))
        logger.info(f"New script activating request received: {event}")

        sfc = await self.scripts_use_case.get_active_script(sfc_id=event.script_for_campaign_id)

        if sfc.done:
            logger.error(f"SFC {sfc.id} is done, skipping")
            return

        return await self.process_script(sfc)

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
        # error = False
        # for bot in bots:
        #     for chat in target_chats:
        #         try:
        #             await self.workers_use_case.join_chat(worker_id=bot.id, chat=chat)
        #         except ChatJoinError:
        #             error = True
        #             break
        #     if error:
        #         break

        # logger.info(f"Target chats: {target_chats}")
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

        target_chats = await self._get_target_chats(sfc)
        logger.info(f"Target chats: {target_chats}")

        for chat in target_chats:
            logger.info(f"Working with chat {chat}")
            messages = await self.scripts_use_case.start_script(script_id)
            bots_mapping = sfc.bots_mapping
            bots_mapping = {key: await self.workers_use_case.get(value) for key, value in bots_mapping.items()}

            last_message_id: Optional[int] = None
            writable = True
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
                    # SlowModeWaitError: A wait of 3443 seconds is required before sending another message in this chat(caused by SendMessageRequest)
                    new_message_id = await self.workers_use_case.send_message(
                        chat_id=chat,
                        bot_id=worker_id,
                        message=text_to_send,
                        reply_to=last_message_id,
                    )
                    last_message_id = new_message_id
                except Exception as e:  # ChatWriteForbiddenError
                    logger.error(
                        f"There is an error sending message {text_to_send} from bot {worker_id} to {chat}: {type(e).__name__}: {e}",
                        exc_info=True
                    )
                    writable = False
                    break
            if writable:
                logger.info(f"All messages from script {script_id} are sent to chat {chat}")
            else:
                logger.info(f"Skipped chat {chat}")
        logger.info(f"All messages from script {script_id} are sent to all chats")

        await self.scripts_use_case.sfc_done(sfc.id)

    async def _get_random_sleep(self, campaign_id: str):
        delays = await self._get_campaign_delay(campaign_id)
        return randint(delays[0], delays[1])
