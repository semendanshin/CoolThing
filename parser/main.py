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
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)

# class MyClient(Client):
#     async def custom_start(self):
#         """
#         Custom start method to avoid auto authorization
#
#         :return:
#         """
#         await self.connect()
#         await self.initialize()
#
#
# async def get_session_string() -> str:
#     app = MyClient("my_account", api_id, api_hash, in_memory=True)
#     await app.custom_start()
#
#     sent_code = await app.send_code(phone_number)
#
#     input_code = input("Enter the code: ")
#
#     try:
#         await app.sign_in(phone_number, sent_code.phone_code_hash, input_code)
#     except SessionPasswordNeeded as e:
#         password = input(f"Enter 2FA password: ")
#         await app.check_password(password)
#
#     return await app.storage.export_session_string()


async def main():
    chats = [-4270454508]

    stemmer = SnowballStemmer("russian")
    positive_key_words = set([stemmer.stem(word) for word in ["квартира", "дом", "снять", "аренда", "арендовать"]])
    negative_key_words = set([stemmer.stem(word) for word in ["продажа", "продать", "сдать", "покупка", "купить"]])

    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")

    event_repository = RabbitMQEventRepository(
        url=rmq_url,
    )

    event_use_cases = EventUseCases(
        event_repository=event_repository,
    )

    main_handler = GroupMessageHandler(
        chats=chats,
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
