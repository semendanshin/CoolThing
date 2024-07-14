from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.models import Worker

from abstractions.repositories import CRUDRepositoryInterface


@dataclass
class WorkerCreateDTO:
    id: str
    app_id: str
    app_hash: str
    session_string: str
    proxy: str
    campaign_id: str
    role: str
    status: str


@dataclass
class WorkerUpdateDTO:
    id: str
    app_id: str
    app_hash: str
    session_string: str
    proxy: str
    campaign_id: str
    role: str
    status: str


class WorkerRepositoryInterface(
    CRUDRepositoryInterface[Worker, WorkerCreateDTO, WorkerUpdateDTO], ABC
):
    @abstractmethod
    async def update_status(self, obj_id: str, status: str) -> None:
        pass
