from dataclasses import dataclass, field

from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import SentCode

from abstractions.repositories.TelegramSessionRepositoryInterface import TelegramSessionRepositoryInterface, \
    TwoFARequiredException, AppIdNotFoundException


class MyClient(Client):
    async def custom_start(self):
        """
        Custom start method to avoid auto authorization

        :return:
        """
        await self.connect()
        await self.initialize()


@dataclass
class ClientData:
    app_id: int
    app_hash: str
    phone: str

    sent_code: SentCode
    client: MyClient


@dataclass
class PyrogramTelegramSessionRepository(
    TelegramSessionRepositoryInterface,
):
    _apps: dict[int, ClientData] = field(default_factory=dict)

    async def send_code(self, app_id: int, app_hash: str, phone: str, proxy: str) -> None:
        app = MyClient(
            name="bot",
            api_id=app_id,
            api_hash=app_hash,
            phone_number=phone,
            in_memory=True,
        )
        await app.custom_start()
        sent_code = await app.send_code(phone)
        self._apps[app_id] = ClientData(app_id, app_hash, phone, sent_code, app)

    async def authorize(self, app_id: int, code: str) -> str:
        app = self._apps.get(app_id)

        if not app:
            raise AppIdNotFoundException

        try:
            await app.client.sign_in(app.phone, app.sent_code.phone_code_hash, code)
        except SessionPasswordNeeded:
            raise TwoFARequiredException

        return await app.client.storage.export_session_string()

    async def authorize_2fa(self, app_id: int, password: str) -> str:
        app = self._apps.get(app_id)

        if not app:
            raise AppIdNotFoundException

        await app.client.check_password(password)
        return await app.client.storage.export_session_string()
