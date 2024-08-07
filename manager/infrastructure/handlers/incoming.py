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

        chat = await self.gpt_use_case.get_chat_by_telegram_chat_id(event.chat_id)

        if not chat:
            logger.info(f"Chat not found: {event.chat_id}")
            return

        await self.gpt_use_case.save_message(chat.id, event.message.text, is_outgoing=False)

        if not chat.auto_reply:
            return

        if self.waiting_for_response.get(event.message.chat_id):
            return

        self.waiting_for_response[event.message.chat_id] = True

        await asyncio.sleep(randint(7, 10))
        await event.client(
            functions.messages.SetTypingRequest(
                peer=event.message.chat_id,
                action=SendMessageTypingAction()
            )
        )

        response = await self.gpt_use_case.generate_response(chat.id)

        await self.gpt_use_case.save_message(chat.id, response, is_outgoing=True)

        self.waiting_for_response[event.message.chat_id] = False

        await asyncio.sleep(randint(3, 10))

        await event.client.send_message(event.chat_id, response)

    def register_handlers(self, app: TelegramClient) -> None:
        app.on(
            events.NewMessage(
                incoming=True,
                outgoing=False,
                func=lambda e: e.message.is_private and e.message.text
            )
        )(self.response_to_user)
