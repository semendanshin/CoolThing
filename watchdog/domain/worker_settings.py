from dataclasses import dataclass


@dataclass(kw_only=True)
class WorkerSettings:
    id: str
    app_id: str
    app_hash: str
    session_string: str
    proxy: str
    campaign_id: str
    role: str
    status: str


@dataclass(kw_only=True)
class ManagerSettings(WorkerSettings):
    welcome_message: str
    model: str
    token: str
    openai_proxy: str
    assistant: str
    service_prompt: str
    typing_and_sending_sleep_from: int
    typing_and_sending_sleep_to: int
    welcome_sleep_from: int
    welcome_sleep_to: int

    def __hash__(self):
        return hash(
            (
                self.id,
                self.app_id,
                self.app_hash,
                self.session_string,
                self.proxy,
                self.campaign_id,
                self.role,
                self.status,
                self.model,
                self.assistant,
                self.openai_proxy,
                self.token,
                self.service_prompt,
                self.welcome_message,
                self.typing_and_sending_sleep_from,
                self.typing_and_sending_sleep_to,
                self.welcome_sleep_from,
                self.welcome_sleep_to,
            )
        )


@dataclass(kw_only=True)
class ParserSettings(WorkerSettings):
    chats: list[str]
    plus_keywords: list[str]
    minus_keywords: list[str]

    def __hash__(self):
        return hash(
            (
                self.id,
                self.app_id,
                self.app_hash,
                self.session_string,
                self.proxy,
                self.campaign_id,
                self.role,
                self.status,
                tuple(self.chats),
                tuple(self.plus_keywords),
                tuple(self.minus_keywords),
            )
        )


@dataclass
class RabbitMQSettings:
    host: str
    port: int
    user: str
    password: str
    vhost: str


@dataclass
class DBSettings:
    host: str
    port: int
    user: str
    password: str
    name: str
