from dataclasses import dataclass

from domain.baseevent import BaseEvent


@dataclass(kw_only=True)
class NewTargetMessage(BaseEvent):
    worker_id: str
    campaign_id: str
    chat_id: int
    username: str
    message: str
