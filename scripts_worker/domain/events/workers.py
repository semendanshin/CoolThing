from dataclasses import dataclass
from typing import Literal, Optional

from domain.events import BaseEvent


@dataclass(kw_only=True)
class WorkerEvent(BaseEvent):
    type: Literal['pause', 'unpause']
    worker_id: str


@dataclass(kw_only=True)
class PauseWorkerEvent(WorkerEvent):
    type: Literal['pause', 'unpause'] = 'pause'

    def __post_init__(self):
        self.type = 'pause'


@dataclass(kw_only=True)
class UnpauseWorkerEvent(WorkerEvent):
    type: Literal['pause', 'unpause'] = 'unpause'

    def __post_init__(self):
        self.type = 'unpause'
