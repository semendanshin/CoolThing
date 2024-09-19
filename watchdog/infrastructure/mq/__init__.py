import asyncio
import logging
import traceback
from dataclasses import field, dataclass
from typing import Callable, Coroutine, Any

import aio_pika
from aio_pika import IncomingMessage
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool

logger = logging.getLogger(__name__)


@dataclass
class RabbitListener:
    url: str
    callback: Callable[[Any], Coroutine[Any, Any, None]]

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

        while self._is_running:
            try:
                async with self.channel_pool.acquire() as channel:  # type: aio_pika.Channel
                    await channel.set_qos(10)

                    exchange = await channel.declare_exchange('scripts_workers_requests', aio_pika.ExchangeType.TOPIC)
                    queue = await channel.declare_queue('workers_queue')
                    await queue.bind(exchange, routing_key='scripts.message_sending')

                    async with queue.iterator() as queue_iter:
                        async for message in queue_iter:  # type: IncomingMessage
                            async with message.process():
                                logger.info(f"Message received: {message.body.decode()}")
                                await self.callback(message)
            except Exception as e:
                logger.error(f"Error consuming message: {e}\n{traceback.format_exc()}")
                await asyncio.sleep(self.period)
                continue
