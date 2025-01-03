from abc import ABC, abstractmethod
from typing import Literal

from abstractions.repositories import CRUDRepositoryInterface
from domain.models import Worker
from domain.dto.worker import WorkerCreateDTO, WorkerUpdateDTO


class WorkersRepositoryInterface(
    CRUDRepositoryInterface[
        Worker, WorkerCreateDTO, WorkerUpdateDTO
    ],
    ABC,
):
    @abstractmethod
    async def update_status(self, obj_id: str, status: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> Worker:
        raise NotImplementedError

    @abstractmethod
    async def get_by_role(self, role: Literal['manager', 'parser']) -> list[Worker]:
        raise NotImplementedError
