import asyncio
import logging

from nltk import SnowballStemmer
from pyrogram import Client
from pyrogram.methods.utilities.idle import idle

from infrastructure.handlers.group_messages.handler import GroupMessageHandler
from infrastructure.repositories.rabbitmq.event import RabbitMQEventRepository
from settings import settings
from usecases.events import EventUseCases

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)


async def main():
    stemmer = SnowballStemmer("russian")
    positive_key_words = set([stemmer.stem(word) for word in settings.parser.keywords.positive])
    negative_key_words = set([stemmer.stem(word) for word in settings.parser.keywords.negative])

    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")

    event_repository = RabbitMQEventRepository(
        url=rmq_url,
        queue=settings.rabbit.queue,
    )

    event_use_cases = EventUseCases(
        event_repository=event_repository,
    )

    main_handler = GroupMessageHandler(
        chats=settings.parser.chats,
        positive_key_words=positive_key_words,
        negative_key_words=negative_key_words,
        event_use_cases=event_use_cases,
    )

    app = Client(
        name="my_account",
        api_id=settings.app.api_id,
        api_hash=settings.app.api_hash,
        session_string=settings.app.session_string,
    )

    main_handler.register_handlers(app)

    await app.start()
    await idle()
    await app.stop()


asyncio.run(main())
