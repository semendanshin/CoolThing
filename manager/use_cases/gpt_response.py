import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from random import randint
from typing import Annotated

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

    typing_sleep_from: int
    typing_sleep_to: int

    sending_sleep_from: int
    sending_sleep_to: int

    batching_sleep: int

    waiting_for_response: dict[int, bool] = field(default_factory=dict)

    waiting_for_new_messages: dict[
        int,
        Annotated[
            datetime,
            "Will generate response on stated datetime"
        ]
    ] = field(default_factory=dict)

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
        async with await self.uow.attach(
                self.messages_repo,
                self.chats_repo,
        ):
            telegram_chat_id = message.chat.id

            chat = await self.chats_repo.get_by_telegram_chat_id(telegram_chat_id)

            if not chat:
                logger.info(f"Chat not found: {telegram_chat_id}")
                return

            await self._save_message(chat.id, message.text, is_outgoing=False)

            if not chat.auto_reply:
                return

            # If the chat is watched by another coroutine (present = watching)
            if until := self.waiting_for_new_messages.get(telegram_chat_id):
                self.waiting_for_new_messages[telegram_chat_id] = until + timedelta(seconds=self.batching_sleep)
                return

            # If the chat is not watched by another coroutine
            if not (until := self.waiting_for_new_messages.get(telegram_chat_id)):
                self.waiting_for_new_messages[telegram_chat_id] = datetime.now() + timedelta(seconds=self.batching_sleep)
                while datetime.now() < until:
                    await asyncio.sleep(1)
                    # If there is a new message in the chat we should wait more
                    until = self.waiting_for_new_messages.get(telegram_chat_id)

                del self.waiting_for_new_messages[telegram_chat_id]

            if self.waiting_for_response.get(message.chat.id):
                return

            self.waiting_for_response[message.chat.id] = True

            await asyncio.sleep(randint(self.typing_sleep_from, self.typing_sleep_to))
            await self.message_helper.set_typing_status(
                chat_id=message.chat.id,
            )

            response = await self._generate_response(chat_id=chat.id)

            await self._save_message(chat.id, response, is_outgoing=True)

            self.waiting_for_response[message.chat.id] = False

            await asyncio.sleep(randint(self.sending_sleep_from, self.sending_sleep_to))
            await self.message_helper.send_message(
                chat_id=message.chat.id,
                text=response,
            )
