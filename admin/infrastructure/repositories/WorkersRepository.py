from dataclasses import dataclass
from typing import Literal

from sqlalchemy import update, select

from domain.dto.worker import WorkerCreateDTO, WorkerUpdateDTO
from infrastructure.entities import Worker
from infrastructure.repositories import AbstractSQLAlchemyRepository

from domain.models import Worker as WorkerModel

from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface


@dataclass
class SQLAlchemyWorkerRepository(
    AbstractSQLAlchemyRepository[
        Worker, WorkerModel, WorkerCreateDTO, WorkerUpdateDTO
    ],
    WorkersRepositoryInterface,
):
    async def get_by_role(self, role: Literal['manager', 'parser']) -> list[WorkerModel]:
        async with self.session_maker() as session:
            entities = (await session.execute(select(Worker).where(Worker.role == role))).scalars().all()
        return [
            self.entity_to_model(entity) for entity in entities
        ]

    async def get_by_username(self, username: str) -> Worker:
        async with self.session_maker() as session:
            return self.entity_to_model(
                (await session.execute(
                    select(Worker).where(Worker.username == username)
                )).scalar_one()
            )

    async def update_status(self, obj_id: str, status: str) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await session.execute(
                    update(Worker).where(Worker.id == obj_id).values(status=status)
                )

    def entity_to_model(self, entity: Worker) -> WorkerModel:
        return WorkerModel(
            id=str(entity.id),
            app_id=entity.app_id,
            app_hash=entity.app_hash,
            session_string=entity.session_string,
            proxy=entity.proxy,
            campaign_id=str(entity.campaign_id) if entity.campaign_id else None,
            role=entity.role,
            status=entity.status,
            username=entity.username,
            bio=entity.bio,
        )

    def model_to_entity(self, model: WorkerModel) -> Worker:
        return Worker(
            id=model.id,
            app_id=model.app_id,
            app_hash=model.app_hash,
            session_string=model.session_string,
            proxy=model.proxy,
            campaign_id=model.campaign_id,
            role=model.role,
            status=model.status,
            username=model.username,
            bio=model.bio,
        )
