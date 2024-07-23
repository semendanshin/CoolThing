import json
import signal

from telegram import Update, InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler


import asyncio
import logging
from dataclasses import field, dataclass
from typing import TypeVar, Callable, Coroutine, Any

import aio_pika
from aio_pika import IncomingMessage
from aio_pika.abc import AbstractRobustConnection, ExchangeType
from aio_pika.pool import Pool

from domain.new_target_message import NewTargetMessage
from settings import settings

handler = TypeVar("handler", bound=Callable[[IncomingMessage], Coroutine[Any, Any, None]])

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


@dataclass
class RabbitListener:
    url: str
    campaign_id: str
    callback: handler

    period: int = 5

    _is_running: bool = field(default=False, init=False)
    _loop: asyncio.AbstractEventLoop = field(default=None, init=False)
    _consume_task: asyncio.Task = field(default=None, init=False)

    connection_pool: Pool = field(init=False)
    channel_pool: Pool = field(init=False)

    def __post_init__(self):
        self.connection_pool = Pool(self._get_connection, max_size=2)
        self.channel_pool = Pool(self._get_channel, max_size=10)

    async def _get_connection(self) -> AbstractRobustConnection:
        return await aio_pika.connect_robust(self.url)

    async def _get_channel(self) -> aio_pika.Channel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    async def start(self):
        if self._is_running:
            logger.warning("Consumer is already running.")
        await self._start()

    async def _start(self):
        if self._loop is None:
            await self._initialize()

        self._is_running = True

        self._consume_task = self._loop.create_task(self._consume(), name="RabbitListener._consume")

        logger.info("Consumer started.")

    async def stop(self):
        if not self._is_running:
            logger.warning("Consumer is not running.")
        await self._stop()

    async def _stop(self):
        self._is_running = False
        self._consume_task.cancel()
        logger.info("Consumer stopped.")

    async def _initialize(self):
        self._loop = asyncio.get_running_loop()

    async def _consume(self):
        if not self._is_running:
            raise Exception("Consumer is not running.")

        async with self.channel_pool.acquire() as channel:  # type: aio_pika.Channel
            await channel.set_qos(10)

            exchange = await channel.declare_exchange('campaign_exchange', ExchangeType.TOPIC)

            queue_name = f'{self.campaign_id}_observers'
            queue = await channel.declare_queue(queue_name, durable=True)
            await queue.bind(exchange, routing_key=f'{self.campaign_id}.parser')

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:  # type: IncomingMessage
                    async with message.process():
                        logger.info(f"Message received: {message.body.decode()}")
                        try:
                            await self.callback(message)
                        except Exception as e:
                            logger.error(f"Error occurred: {e}")
                            logger.debug("Skipping message")
                            raise e


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logger.info("Exiting gracefully")
        self.kill_now = True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    webapp = WebAppInfo(
        url=f"{settings.host}/dashboard",
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Открыть приложение", web_app=webapp),
            ]
        ]
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Админ-панель тут:",
        reply_markup=keyboard,
    )


ADMIN_CHAT_ID = 848643556


@dataclass
class RabbitHandler:
    app: Application

    async def callback(self, message: IncomingMessage):
        event = NewTargetMessage(**json.loads(message.body.decode()))
        logger.info(f"Event received: {event}")
        await self.app.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"New target message detected:\n@{event.username} in <i>{event.chat_id} by {event.worker_id} "
                 f"(campaign: {event.campaign_id})</i>\nMessage:\n{event.message}",
            parse_mode="HTML",
        )


async def main():
    app = Application.builder().token(settings.tg_bot_token).build()

    app.add_handler(
        CommandHandler(
            command="start",
            callback=start,
        )
    )

    rabbit_handler = RabbitHandler(app=app)

    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")
    rabbit_listener = RabbitListener(
        url=rmq_url,
        campaign_id='ce604c0e-e27e-415b-b6f0-2f678ae59a16',
        callback=rabbit_handler.callback,
    )

    await rabbit_listener.start()

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    logger.info("Bot started")
    killer = GracefulKiller()
    while not killer.kill_now:
        await asyncio.sleep(1)

    await app.updater.stop()
    await app.stop()
    await app.shutdown()

    await rabbit_listener.stop()


if __name__ == "__main__":
    asyncio.run(main())
