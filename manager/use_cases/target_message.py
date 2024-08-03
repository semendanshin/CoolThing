import asyncio
import json
import logging
import uuid
from dataclasses import dataclass
from random import randint

from aio_pika import IncomingMessage
from pyrogram import Client

from abstractions.repositories.chat import ChatRepositoryInterface, ChatCreateDTO
from abstractions.repositories.message import MessageRepositoryInterface, MessageCreateDTO
from domain.new_target_message import NewTargetMessage

logger = logging.getLogger(__name__)


@dataclass
class TargetMessageEventHandler:
    chats_repo: ChatRepositoryInterface
    messages_repo: MessageRepositoryInterface

    app: Client

    welcome_message: str
    campaign_id: str
    worker_id: str

    async def new_target_message(self, message: IncomingMessage) -> None:
        event = NewTargetMessage(**json.loads(message.body.decode()))
        logger.info(f"New target message received: {event}")

        try:
            telegram_chat_id = (await self.app.get_chat(event.username)).id
        except Exception as e:
            logger.error(f"Error getting chat: {e}")
            return

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

        await asyncio.sleep(15)

        sent_message = await self.app.send_message(chat_id=event.username, text=self.welcome_message)

        logger.debug(f"Welcome message sent: {sent_message}")

        await self.messages_repo.create(
            MessageCreateDTO(
                chat_id=chat_id,
                text=self.welcome_message,
                is_outgoing=True,
            )
        )

        logger.debug("Chat created")
