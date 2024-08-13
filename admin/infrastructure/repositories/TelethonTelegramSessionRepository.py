import logging
import re
from dataclasses import dataclass, field

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession

from abstractions.repositories.TelegramSessionRepositoryInterface import TelegramSessionRepositoryInterface, \
    AppIdNotFoundException, TwoFARequiredException

logger = logging.getLogger(__name__)


@dataclass
class ClientData:
    app_id: int
    app_hash: str
    phone: str
    proxy: dict

    client: TelegramClient


@dataclass
class TelethonTelegramSessionRepository(
    TelegramSessionRepositoryInterface,
):
    _apps: dict[int, ClientData] = field(default_factory=dict)

    @staticmethod
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

    async def send_code(self, app_id: int, app_hash: str, phone: str, proxy: str = None) -> None:
        proxy = self.parse_proxy(proxy) if proxy else None
        app = TelegramClient(
            StringSession(),
            api_id=app_id,
            api_hash=app_hash,
            proxy=proxy,
        )

        await app.connect()
        await app.send_code_request(phone)

        self._apps[app_id] = ClientData(
            app_id=app_id,
            app_hash=app_hash,
            phone=phone,
            proxy=proxy,
            client=app,
        )

    async def authorize(self, app_id: int, code: str) -> str:
        app = self._apps.get(app_id)

        if not app:
            raise AppIdNotFoundException

        try:
            await app.client.sign_in(code=code)
        except SessionPasswordNeededError:
            raise TwoFARequiredException

        return app.client.session.save()

    async def authorize_2fa(self, app_id: int, password: str) -> str:
        app = self._apps.get(app_id)

        if not app:
            raise AppIdNotFoundException

        await app.client.sign_in(password=password)
        return app.client.session.save()
