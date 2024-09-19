import dataclasses
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime

import aio_pika
from aio_pika.abc import AbstractRobustConnection, ExchangeType
from aio_pika.pool import Pool

from domain.events import BaseEvent
from abstractions.repositories.EventsRepositoryInterface import EventsRepositoryInterface

logger = logging.getLogger(__name__)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return str(o)
        return super().default(o)


@dataclass
class RabbitMQEventsRepository(EventsRepositoryInterface):
    url: str

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

    async def publish(self, event: BaseEvent):
        async with self.channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange('scripts_workers_requests', ExchangeType.TOPIC)
            routing_key = f"scripts.message_sending"
            await exchange.publish(
                aio_pika.Message(
                    body=json.dumps(event, cls=EnhancedJSONEncoder).encode(),
                ),
                routing_key=routing_key,
            )

            logger.debug(f"Published event: {event}")
