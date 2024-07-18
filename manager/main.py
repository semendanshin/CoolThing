import asyncio
import json
import logging
from collections import defaultdict
from dataclasses import dataclass, asdict

from aio_pika.message import IncomingMessage
from openai import OpenAI
from pyrogram import Client, idle, filters
from pyrogram.enums import ChatAction
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message as PyrogramMessage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from abstractions.repositories.chat import ChatRepositoryInterface, ChatCreateDTO
from abstractions.repositories.message import MessageCreateDTO, MessageRepositoryInterface
from domain.new_target_message import NewTargetMessage
from infrastructure.handlers.incoming import IncomingMessageHandler
from infrastructure.openai import GPTRepository
from infrastructure.rabbit import RabbitListener
from infrastructure.sqlalchemy import SQLAlchemyMessagesRepository, SQLAlchemyChatsRepository
from settings import settings

from typing import Literal

from use_cases.gpt_response import GPTUseCase
from use_cases.target_message import TargetMessageEventHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


async def main():

    app = Client(
        name="my_account",
        api_id=settings.app.api_id,
        api_hash=settings.app.api_hash,
        session_string=settings.app.session_string,
    )

    db_url = (f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}"
              f"@{settings.db.host}:{settings.db.port}/{settings.db.name}")

    engine = create_async_engine(db_url, echo=True)
    session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    messages_repo = SQLAlchemyMessagesRepository(
        session_maker=session_maker,
    )
    chats_repo = SQLAlchemyChatsRepository(
        session_maker=session_maker,
    )

    gpt_repo = GPTRepository(
        api_key=settings.openai.api_key,
        model=settings.openai.model,
    )

    gpt_use_case = GPTUseCase(
        messages_repo=messages_repo,
        gpt_repo=gpt_repo,
        chats_repo=chats_repo,
    )

    target_message_use_case = TargetMessageEventHandler(
        chats_repo=chats_repo,
        messages_repo=messages_repo,
        app=app,
        welcome_message=settings.welcome_message,
        campaign_id="971ed010-0152-4125-bdd1-b313d9ceeb7c",
        worker_id=settings.app.id,
    )

    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")

    listener = RabbitListener(
        url=rmq_url,
        queue_name=settings.rabbit.queue,
        callback=target_message_use_case.new_target_message,
    )

    incoming_message_handler = IncomingMessageHandler(
        gpt_use_case=gpt_use_case,
        chats=[6043397367, 280584516, 5380348133]
    )

    incoming_message_handler.register_handlers(app)

    await listener.start()

    await app.start()
    logger.info("Bot started")

    await idle()

    logger.info("Bot stopped")
    await app.stop()

    await listener.stop()


if __name__ == "__main__":
    asyncio.run(main())
