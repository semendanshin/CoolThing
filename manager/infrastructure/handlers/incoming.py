import asyncio
import logging
from dataclasses import dataclass, field
from random import randint

from telethon.tl.types import SendMessageTypingAction

from use_cases.gpt_response import GPTUseCase

from telethon import TelegramClient, events, functions

logger = logging.getLogger(__name__)


@dataclass
class IncomingMessageHandler:
    gpt_use_case: GPTUseCase

    waiting_for_response: dict[int, bool] = field(default_factory=dict)

    async def response_to_user(self, event: events.NewMessage.Event) -> None:
        logger.info(f"Received message: {event.message.text}")

        await self.gpt_use_case.handle_incoming_message(event.message)

    def register_handlers(self, app: TelegramClient) -> None:
        app.on(
            events.NewMessage(
                incoming=True,
                outgoing=False,
                func=lambda e: e.message.is_private and e.message.text
            )
        )(self.response_to_user)
