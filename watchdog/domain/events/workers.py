from dataclasses import dataclass
from typing import TypeVar, Literal

from domain.events import BaseEvent


@dataclass(kw_only=True)
class PauseWorkerEvent(BaseEvent):
    type: Literal['pause', 'unpause']
    worker_id: str
