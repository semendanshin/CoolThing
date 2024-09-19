from dataclasses import fields

from abstractions.repositories.BundlesRepositoryInterface import BundlesRepositoryInterface
from domain.dto.bundle import BundleCreateDTO, BundleUpdateDTO
from domain.models import Bundle as BundleModel
from domain.models import Worker as WorkerModel
from infrastructure.entities import BotsBundle
from infrastructure.entities.sqlalchemy import BotBundleMapping
from infrastructure.repositories.sqlalchemy import AbstractSQLAlchemyRepository


class BundlesRepository(
    AbstractSQLAlchemyRepository[
        BotsBundle, BundleModel, BundleCreateDTO, BundleUpdateDTO
    ],
    BundlesRepositoryInterface,
):
    bundles_workers_mapping_entity = BotBundleMapping

    async def add_worker_to_bundle(self, worker_id: str, bundle_id: str) -> None:
        mapping_instance = BotBundleMapping(
            bundle_id=bundle_id,
            bot_id=worker_id
        )
        async with self.session_maker() as session:
            async with session.begin():
                session.add(mapping_instance)

    def entity_to_model(self, entity: BotsBundle) -> BundleModel:
        return BundleModel(
            id=str(entity.id),
            name=entity.name,
            bots=[WorkerModel(**{field.name: getattr(worker, field.name) for field in fields(WorkerModel)}) for worker
                  in entity.bots],
        )

    def model_to_entity(self, model: BundleModel) -> BotsBundle:
        return BotsBundle(
            id=model.id,
            name=model.name,
        )
