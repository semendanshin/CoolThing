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
    model: str
    assistant: str
    token: str
    service_prompt: str
    welcome_message: str

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
                self.token,
                self.service_prompt,
                self.welcome_message,
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
