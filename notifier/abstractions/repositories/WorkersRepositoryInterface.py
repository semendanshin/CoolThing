from abc import ABC

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.worker import WorkerCreateDTO, WorkerUpdateDTO
from domain.models import Worker


class WorkersRepositoryInterface(
    CRUDRepositoryInterface[
        Worker, WorkerCreateDTO, WorkerUpdateDTO
    ],
    ABC,
):
    ...
