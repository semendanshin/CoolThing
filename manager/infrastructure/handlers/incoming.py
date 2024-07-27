import asyncio
import logging
import uuid
from dataclasses import dataclass, field
from random import randint

from abstractions.repositories.message import MessageCreateDTO
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from use_cases.gpt_response import GPTUseCase

logger = logging.getLogger(__name__)


@dataclass
class IncomingMessageHandler:
    gpt_use_case: GPTUseCase
    chats: list[int]

    waiting_for_response: dict[int, bool] = field(default_factory=dict)

    async def response_to_user(self, client: Client, message: Message) -> None:
        logger.info(f"Received message: {message.text}")

        chat = await self.gpt_use_case.chats_repo.get_by_telegram_chat_id(message.chat.id)

        if not chat:
            logger.info(f"Chat not found: {message.chat.id}")
            return

        await self.gpt_use_case.messages_repo.create(
            MessageCreateDTO(
                id=str(uuid.uuid4()),
                chat_id=chat.id,
                text=message.text,
                is_outgoing=False,
            )
        )

        if self.waiting_for_response.get(message.chat.id):
            return

        self.waiting_for_response[message.chat.id] = True

        await asyncio.sleep(randint(7, 10))
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        # response = await self.gpt_use_case.generate_response(
        #     chat_id=message.chat.id,
        #     text=message.text,
        # )

        messages = await self.gpt_use_case.messages_repo.get_by_chat_id(chat.id)
        response = await self.gpt_use_case.gpt_repo.generate_response(messages)
        await self.gpt_use_case.messages_repo.create(
            MessageCreateDTO(
                id=str(uuid.uuid4()),
                chat_id=chat.id,
                text=response,
                is_outgoing=True,
            )
        )

        self.waiting_for_response[message.chat.id] = False

        await asyncio.sleep(randint(3, 10))

        await message.reply_text(response)

    def register_handlers(self, app: Client) -> None:
        app.add_handler(
            MessageHandler(
                self.response_to_user,
                filters.text & ~filters.me,
                # filters.text & ~filters.me & filters.chat(self.chats),
            ),
        )
