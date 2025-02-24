from pathlib import Path
from typing import Type, Tuple, Annotated
from urllib.parse import quote_plus

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class ScriptProcessSettings(BaseSettings):
    decision_delay: Annotated[int, 'Time in seconds to mark smth as failed'] = 30


class ScriptsDBSettings(BaseSettings):
    user: str
    password: SecretStr
    host: str
    port: int
    name: str

    def __post_init__(self):
        self.password = SecretStr(quote_plus(self.password.get_secret_value()))
        self.user = quote_plus(self.user)

    @property
    def url(self):
        return f"mongodb://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}?authSource=admin&directConnection=true"


class DBSettings(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: SecretStr

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    process: ScriptProcessSettings
    db: DBSettings
    scripts_db: ScriptsDBSettings

    debug: bool = True

    model_config = SettingsConfigDict(
        extra='ignore',
        json_file=Path(__file__).parent / 'settings.json',
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
