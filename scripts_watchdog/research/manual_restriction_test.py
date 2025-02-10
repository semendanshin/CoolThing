import asyncio
from pathlib import Path
from typing import Optional
from typing import Type, Tuple

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource
from telethon import TelegramClient as Client
from telethon.sessions import StringSession


class Settings(BaseSettings):
    api_id: int
    api_hash: str
    session: SecretStr
    proxy: Optional[str] = None

    model_config = SettingsConfigDict(
        extra='ignore',
        json_file=Path(__file__).parent / 'settings_files' / 'manual.settings.json',
        json_file_encoding='utf-8',
    )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (JsonConfigSettingsSource(settings_cls),)


settings = Settings()


async def main(settings: Settings):
    client = Client(
        api_hash=settings.api_hash,
        api_id=settings.api_id,
        session=StringSession(settings.session.get_secret_value()),
        proxy=settings.proxy,
    )
    chat = "https://t.me/lolingstones"

    await client.connect()
    try:
        await client.send_message(chat, "hi")

    finally:
        await client.disconnect()

    #
    # await client.connect()
    # try:
    #     entity = await client.get_entity(chat)
    #
    #     await client(JoinChannelRequest(entity))  # noqa
    #     await client.disconnect()
    # except Exception as e:
    #     await client.disconnect()


asyncio.run(main(settings))
