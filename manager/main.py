import asyncio
import logging
import re
import signal

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from telethon import TelegramClient
from telethon.sessions import StringSession

from infrastructure.handlers.incoming import IncomingMessageHandler
from infrastructure.openai import GPTRepository, AssistantRepository
from infrastructure.rabbit import RabbitListener
from infrastructure.sqlalchemy import SQLAlchemyMessagesRepository, SQLAlchemyChatsRepository
from settings import settings
from use_cases.gpt_response import GPTUseCase
from use_cases.target_message import TargetMessageEventHandler

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",

)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

logging.getLogger("telethon").setLevel(logging.WARNING)

logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logger.info("Exiting gracefully")
        self.kill_now = True


async def main():
    def parse_proxy(proxy: str) -> dict:
        scheme, username, password, host, port = re.match(
            r"^(?P<scheme>http|socks5|socks4)://(?:(?P<username>[^:]+):(?P<password>[^@]+)@)?(?P<host>[^:]+):(?P<port>\d+)$",
            proxy,
        ).groups()
        proxy_dict = {
            "proxy_type": scheme,
            "addr": host,
            "port": int(port),
        }
        if username:
            proxy_dict["username"] = username
            proxy_dict["password"] = password
        logger.info(f"Using proxy: {proxy_dict}")
        return proxy_dict

    proxy = parse_proxy(settings.app.proxy) if settings.app.proxy else None

    app = TelegramClient(
        session=StringSession(settings.app.session_string),
        api_id=settings.app.api_id,
        api_hash=settings.app.api_hash,
        proxy=proxy,
    )
    await app.connect()

    db_url = (f"postgresql+asyncpg://{settings.db.user}:{settings.db.password}"
              f"@{settings.db.host}:{settings.db.port}/{settings.db.name}")

    engine = create_async_engine(db_url, echo=False)
    session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    messages_repo = SQLAlchemyMessagesRepository(
        session_maker=session_maker,
    )
    chats_repo = SQLAlchemyChatsRepository(
        session_maker=session_maker,
    )

    if settings.openai.assistant:
        gpt_repo = AssistantRepository(
            api_key=settings.openai.api_key,
            model=settings.openai.model,
            assistant_id=settings.openai.assistant,
            proxy=settings.openai.proxy,
        )
    else:
        gpt_repo = GPTRepository(
            api_key=settings.openai.api_key,
            model=settings.openai.model,
            service_prompt=settings.openai.service_prompt,
            proxy=settings.openai.proxy,
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
        campaign_id=settings.campaign_id,
        worker_id=settings.app.id,
    )

    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")

    listener = RabbitListener(
        url=rmq_url,
        campaign_id=settings.campaign_id,
        callback=target_message_use_case.new_target_message,
    )

    incoming_message_handler = IncomingMessageHandler(
        gpt_use_case=gpt_use_case,
    )

    incoming_message_handler.register_handlers(app)

    await app.start()
    logger.info("Bot started")

    await listener.start()

    killer = GracefulKiller()
    future = asyncio.ensure_future(app.run_until_disconnected())

    while not killer.kill_now:
        await asyncio.sleep(1)

    await app.disconnect()

    await listener.stop()

    future.cancel()

    logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
