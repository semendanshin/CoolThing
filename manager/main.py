import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar, Coroutine

import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.message import IncomingMessage
from aio_pika.pool import Pool
from pyrogram import Client, idle

from domain.new_target_message import NewTargetMessage
from settings import settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("aio_pika").setLevel(logging.WARNING)
logging.getLogger("aiormq").setLevel(logging.WARNING)

app = Client(
    name="my_account",
    api_id=settings.app.api_id,
    api_hash=settings.app.api_hash,
    session_string=settings.app.session_string,
)


handler = TypeVar("handler", bound=Callable[[IncomingMessage], Coroutine[Any, Any, None]])


@dataclass
class RabbitListener:
    url: str
    queue_name: str
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

            queue = await channel.declare_queue(
                self.queue_name, durable=False, auto_delete=False,
            )

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:  # type: IncomingMessage
                    async with message.process():
                        logger.info(f"Message received: {message.body.decode()}")
                        await self.callback(message)


async def main():
    rmq_url = (f"amqp://{settings.rabbit.user}:{settings.rabbit.password}@"
               f"{settings.rabbit.host}:{settings.rabbit.port}/{settings.rabbit.vhost}")

    async def callback(message: IncomingMessage) -> None:
        event = NewTargetMessage(**json.loads(message.body.decode()))
        logger.info(f"New target message received: {event}")
        message = await app.send_message(chat_id=event.username, text=settings.welcome_message)
        logger.info(f"Message sent: {message}")

    listener = RabbitListener(
        url=rmq_url,
        queue_name=settings.rabbit.queue,
        callback=callback,
    )

    await listener.start()

    await app.start()
    await idle()
    await app.stop()

    await listener.stop()


if __name__ == "__main__":
    asyncio.run(main())