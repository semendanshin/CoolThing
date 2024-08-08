import asyncio
import json
import logging
import uuid
from dataclasses import dataclass
from random import randint
from typing import Annotated

from aio_pika import IncomingMessage

from abstractions.helpers.message import TelegramClientWrapper
from abstractions.repositories import UOWInterface
from abstractions.repositories.chat import ChatRepositoryInterface, ChatCreateDTO
from abstractions.repositories.message import MessageRepositoryInterface, MessageCreateDTO
from domain.new_target_message import NewTargetMessage

logger = logging.getLogger(__name__)


@dataclass
class TargetMessageEventHandler:
    chats_repo: ChatRepositoryInterface
    messages_repo: MessageRepositoryInterface

    message_helper: TelegramClientWrapper

    welcome_message: str
    campaign_id: str
    worker_id: str

    uow: UOWInterface

    welcome_sleep_from: Annotated[int, "in seconds"]
    welcome_sleep_to: Annotated[int, "in seconds"]

    async def new_target_message(self, message: IncomingMessage) -> None:
        event = NewTargetMessage(**json.loads(message.body.decode()))
        logger.info(f"New target message received: {event}")

        try:
            telegram_chat_id = await self.message_helper.get_chat_id(event.username)
        except Exception as e:
            logger.error(f"Error getting chat: {e}")
            return

        async with self.uow.begin(
            self.chats_repo,
            self.messages_repo,
        ):
            chat = await self.chats_repo.get_by_telegram_chat_id(telegram_chat_id)
            if chat:
                logger.info(f"Chat already exists: {chat}")
                return

            chat_id = str(uuid.uuid4())
            await self.chats_repo.create(
                ChatCreateDTO(
                    id=chat_id,
                    campaign_id=self.campaign_id,
                    telegram_chat_id=telegram_chat_id,
                    worker_id=self.worker_id,
                    username=event.username,
                    status="active",
                    lead_message=event.message,
                    lead_chat_id=str(event.chat_id),
                )
            )

            logger.debug("Chat created")

            await asyncio.sleep(self.get_random_sleep())

            sent_message = await self.message_helper.send_message(
                telegram_chat_id,
                self.welcome_message,
            )

            logger.debug(f"Welcome message sent: {sent_message}")

            await self.messages_repo.create(
                MessageCreateDTO(
                    chat_id=chat_id,
                    text=self.welcome_message,
                    is_outgoing=True,
                )
            )

            logger.debug("Chat created")

    def get_random_sleep(self) -> int:
        return randint(self.welcome_sleep_from, self.welcome_sleep_to)
