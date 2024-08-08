import asyncio
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import randint

from pyrogram.types import Message

from abstractions.helpers.message import MessageHelperInterface
from abstractions.repositories import UOWInterface
from abstractions.repositories.chat import ChatRepositoryInterface
from abstractions.repositories.gpt import GPTRepositoryInterface
from abstractions.repositories.message import MessageRepositoryInterface, MessageCreateDTO

logger = logging.getLogger(__name__)


@dataclass
class GPTUseCase:
    gpt_repo: GPTRepositoryInterface
    messages_repo: MessageRepositoryInterface
    chats_repo: ChatRepositoryInterface

    message_helper: MessageHelperInterface

    uow: UOWInterface

    typing_and_sending_sleep_from: int
    typing_and_sending_sleep_to: int

    batching_sleep: int

    waiting_for_new_messages: dict[
        int, datetime
    ] = field(default_factory=lambda: defaultdict(lambda: datetime.now() - timedelta(seconds=2)))

    async def _save_message(self, chat_id: str, text: str, is_outgoing: bool) -> None:
        await self.messages_repo.create(
            MessageCreateDTO(
                chat_id=chat_id,
                text=text,
                is_outgoing=is_outgoing,
            )
        )

    async def _generate_response(self, chat_id: str) -> str:
        messages = await self.messages_repo.get_by_chat_id(chat_id)
        response = await self.gpt_repo.generate_response(messages)
        return response

    async def handle_incoming_message(self, message: Message) -> None:
        telegram_chat_id = message.chat.id
        chat = await self.chats_repo.get_by_telegram_chat_id(telegram_chat_id)

        # if we are batching messages now, that means that we already opened a transaction.
        # So we can just add messages to the transaction and commit it later
        if datetime.now() <= self.waiting_for_new_messages[message.chat.id]:
            await self._save_message(chat.id, message.text, is_outgoing=False)
            logger.debug(f"Batching messages for chat: {telegram_chat_id}")
            self.waiting_for_new_messages[telegram_chat_id] = datetime.now() + timedelta(
                seconds=self.batching_sleep
            )
            return

        # if we are not batching messages, we need to open a transaction
        async with self.uow.begin(
                self.messages_repo,
                self.chats_repo,
        ):

            if not chat:
                logger.info(f"Chat not found: {telegram_chat_id}")
                return

            await self._save_message(chat.id, message.text, is_outgoing=False)

            if not chat.auto_reply:
                logger.info(f"Auto reply disabled for chat: {telegram_chat_id}")
                return

            self.waiting_for_new_messages[telegram_chat_id] = datetime.now() + timedelta(
                seconds=self.batching_sleep)

            while datetime.now() <= self.waiting_for_new_messages[telegram_chat_id]:
                await asyncio.sleep(1)

            await asyncio.sleep(self.get_random_sleep())
            await self.message_helper.set_typing_status(
                chat_id=message.chat.id,
            )

            sleep = asyncio.sleep(self.get_random_sleep())
            task = asyncio.create_task(sleep)

            response = await self._generate_response(chat_id=chat.id)

            await self._save_message(chat.id, response, is_outgoing=True)

            await task

            await self.message_helper.send_message(
                chat_id=message.chat.id,
                text=response,
            )

    def get_random_sleep(self):
        return randint(self.typing_and_sending_sleep_from, self.typing_and_sending_sleep_to)
