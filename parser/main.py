import asyncio
import logging
import re
import signal

from nltk import SnowballStemmer

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import Chat, Updates

from infrastructure.handlers.group_messages.handler import GroupMessageHandler
from infrastructure.repositories.rabbitmq.event import RabbitMQEventRepository
from settings import settings
from usecases.events import EventUseCases

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger("telethon").setLevel(logging.WARNING)

logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logger.info("Exiting gracefully")
        self.kill_now = True


async def join_chats(client: TelegramClient, chats: list[str]):
    for i, chat in enumerate(chats):
        try:
            updates: Updates = await client(JoinChannelRequest(
                channel=chat,
            ))
        except Exception as e:
            logger.error(f"Error while joining chat {chat}: {e}")
            continue
        else:
            chat_obj = updates.chats[0]
            chat_id = chat_obj.id
            chat_title = chat_obj.title
            logger.info(f"Joined chat {chat_title} with id {chat_id}")
            chats[i] = chat_id
    return


async def main():
    stemmer = SnowballStemmer("russian")
    positive_key_words = set([stemmer.stem(word) for word in settings.parser.keywords.positive])
    negative_key_words = set([stemmer.stem(word) for word in settings.parser.keywords.negative])

    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")

    event_repository = RabbitMQEventRepository(
        url=rmq_url,
        campaign_id=settings.rabbit.campaign_id,
    )

    event_use_cases = EventUseCases(
        event_repository=event_repository,
    )

    main_handler = GroupMessageHandler(
        chats=settings.parser.chats,
        positive_key_words=positive_key_words,
        negative_key_words=negative_key_words,
        event_use_cases=event_use_cases,
        worker_id=settings.app.id,
        campaign_id=settings.rabbit.campaign_id,
    )

    if settings.app.proxy:
        scheme, username, password, host, port = re.match(
            r"^(?P<scheme>http|socks5|socks4)://(?:(?P<username>[^:]+):(?P<password>[^@]+)@)?(?P<host>[^:]+):(?P<port>\d+)$",
            settings.app.proxy
        ).groups()
        proxy = {
            "scheme": scheme,
            "hostname": host,
            "port": int(port),
        }
        if username:
            proxy["username"] = username
            proxy["password"] = password
        logger.info(f"Using proxy: {proxy}")
    else:
        proxy = None

    app = TelegramClient(
        StringSession(settings.app.session_string),
        api_id=settings.app.api_id,
        api_hash=settings.app.api_hash,
        proxy=proxy,
    )

    main_handler.register_handlers(app)

    await app.start()
    await join_chats(app, settings.parser.chats)

    future = asyncio.ensure_future(app.run_until_disconnected())

    killer = GracefulKiller()

    while not killer.kill_now:
        await asyncio.sleep(1)

    await app.disconnect()
    await future

    logger.info("Exiting.")


asyncio.run(main())
