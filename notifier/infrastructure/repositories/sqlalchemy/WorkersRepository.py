from dataclasses import dataclass

from abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
from domain.dto.worker import WorkerCreateDTO, WorkerUpdateDTO
from domain.models import Worker as WorkerModel
from infrastructure.entities.sqlalchemy import Worker
from infrastructure.repositories.sqlalchemy import AbstractSQLAlchemyRepository


@dataclass
class SQLAlchemyWorkerRepository(
    AbstractSQLAlchemyRepository[
        Worker, WorkerModel, WorkerCreateDTO, WorkerUpdateDTO
    ],
    WorkersRepositoryInterface,
):
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
            chats=entity.chats,
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
            chats=model.chats,
        )
