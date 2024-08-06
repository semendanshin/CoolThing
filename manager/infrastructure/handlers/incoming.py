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

        await self.gpt_use_case.handle_incoming_message(message)

    def register_handlers(self, app: Client) -> None:
        app.add_handler(
            MessageHandler(
                self.response_to_user,
                filters.text & ~filters.me,
                # filters.text & ~filters.me & filters.chat(self.chats),
            ),
        )
