import logging
import re
from dataclasses import dataclass
from typing import Optional

from telethon import TelegramClient as Client
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from abstractions.repositories.TelegramMessagesRepositoryInterface import TelegramMessagesRepositoryInterface
from domain.models import Worker
from infrastructure.repositories.telegram.exceptions import ChatJoinError, UnhandlableError

logger = logging.getLogger(__name__)
client_logger = logger.getChild("client")
client_logger.setLevel(logging.ERROR)


@dataclass
class TelethonTelegramMessagesRepository(
    TelegramMessagesRepositoryInterface,
):
    async def join_chat(self, worker: Worker, chat: str | int):
        logger.info(f"Joining chat {chat} with bot {worker.username} ({worker.id})")

        client = Client(
            session=StringSession(worker.session_string),
            api_id=int(worker.app_id),
            api_hash=worker.app_hash,
            base_logger=client_logger,
        )

        await client.connect()
        try:
            entity = await client.get_entity(chat)

            await client(JoinChannelRequest(entity))  # noqa
            await client.disconnect()
        except Exception as e:
            await client.disconnect()
            raise ChatJoinError(
                f"There is an error joining chat {chat} with bot {worker.username} ({worker.id}):"
                f" {type(e).__name__}: {e}"
            )

    async def send_message(
            self,
            app_id: str,
            app_hash: str,
            session_string: str,
            chat_id: str,
            text: str,
            reply_to: int,
            proxy: str,
            retry: int = 0,
    ) -> int:
        if not app_id or not app_hash or not session_string:
            raise ValueError("app_id, app_hash and session_string are required")

        client = Client(
            session=StringSession(session_string),
            api_id=int(app_id),
            api_hash=app_hash,
            base_logger=client_logger,
            proxy=self.parse_proxy(proxy),
            auto_reconnect=False,
        )
        logger.info(f"Client instantiated, client id is {id(client)}")

        try:
            await client.connect()
            logger.info("Client connected")

            message = await client.send_message(chat_id, text, reply_to=reply_to)
            logger.info('Message sent')

            await client.disconnect()
            logger.info("Client disconnected")
            return message.id
        except RuntimeError as e:
            await client.disconnect()
            if retry > 5:
                logger.error("Cannot connect to Telegram")
                raise UnhandlableError from e

            return await self.send_message(
                app_id=app_id,
                app_hash=app_hash,
                session_string=app_hash,
                chat_id=chat_id,
                text=text,
                reply_to=reply_to,
                proxy=proxy,
                retry=retry + 1,
            )

    @staticmethod
    def parse_proxy(proxy_string: Optional[str]) -> Optional[tuple]:
        if not proxy_string:
            return

        # Regex to parse the proxy string
        pattern = re.compile(
            r"^(?P<protocol>http|socks5|socks4)://(?P<username>.+?):(?P<password>.+?)@(?P<host>.+?):(?P<port>\d+)$"
        )
        match = pattern.match(proxy_string)
        if not match:
            raise ValueError("Invalid proxy format")

        # Extracting components
        components = match.groupdict()
        protocol = components["protocol"]
        username = components["username"]
        password = components["password"]
        host = components["host"]
        port = int(components["port"])

        # Map protocol to PySocks format
        proxy_type = {
            "http": "HTTP",
            "socks5": "SOCKS5",
            "socks4": "SOCKS4"
        }.get(protocol, None)

        if not proxy_type:
            raise ValueError("Unsupported proxy protocol")

        # PySocks/Telethon-compatible format
        proxy = (proxy_type, host, port, True, username, password)
        return proxy
