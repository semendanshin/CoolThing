import logging
from dataclasses import dataclass, field

from telethon import TelegramClient, events

from use_cases.gpt_response import GPTUseCase

logger = logging.getLogger(__name__)


@dataclass
class IncomingMessageHandler:
    gpt_use_case: GPTUseCase

    waiting_for_response: dict[int, bool] = field(default_factory=dict)

    async def response_to_user(self, event: events.NewMessage.Event) -> None:
        logger.info(f"Received message: {event.message.text}")

        await self.gpt_use_case.handle_incoming_message(
            text=event.message.text,
            telegram_chat_id=event.chat_id,
        )

    def register_handlers(self, app: TelegramClient) -> None:
        app.on(
            events.NewMessage(
                incoming=True,
                outgoing=False,
                func=lambda e: e.message.is_private and e.message.text
            )
        )(self.response_to_user)
