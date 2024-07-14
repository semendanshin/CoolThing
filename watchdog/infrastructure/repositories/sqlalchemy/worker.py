from dataclasses import dataclass

from sqlalchemy import update

from domain.models import Worker as WorkerModel
from infrastructure.repositories.sqlalchemy.abstract import AbstractSQLAlchemyRepository
from infrastructure.repositories.sqlalchemy.entities import Worker

from abstractions.repositories.worker import WorkerCreateDTO, WorkerUpdateDTO, WorkerRepositoryInterface


@dataclass
class SQLAlchemyWorkerRepository(
    AbstractSQLAlchemyRepository[
        Worker, WorkerModel, WorkerCreateDTO, WorkerUpdateDTO
    ],
    WorkerRepositoryInterface,
):

    def entity_to_model(self, entity: Worker) -> WorkerModel:
        return WorkerModel(
            id=entity.id,
            app_id=entity.app_id,
            app_hash=entity.app_hash,
            session_string=entity.session_string,
            proxy=entity.proxy,
            campaign_id=entity.campaign_id,
            role=entity.role,
            status=entity.status,
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
        )

    async def update_status(self, obj_id: str, status: str) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await session.execute(
                    update(Worker).where(Worker.id == obj_id).values(status=status)
                )
