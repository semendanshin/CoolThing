import logging
from abc import abstractmethod
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from abstractions.repositories import CRUDRepositoryInterface

logger = logging.getLogger(__name__)


@dataclass
class AbstractSQLAlchemyRepository[Entity, Model, CreateDTO, UpdateDTO](
    CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO]
):
    session_maker: async_sessionmaker

    async def create(self, obj: CreateDTO) -> None:
        async with self.session_maker() as session:
            session.add(self.model_to_entity(obj))
            await session.commit()

    async def get(self, obj_id: str) -> Model:
        async with self.session_maker() as session:
            return self.entity_to_model(await session.get(Entity, obj_id))

    async def update(self, obj: UpdateDTO) -> None:
        async with self.session_maker() as session:
            await session.merge(self.model_to_entity(obj))
            await session.commit()

    async def delete(self, obj_id: str) -> None:
        async with self.session_maker() as session:
            await session.delete(await session.get(Entity, obj_id))
            await session.commit()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        async with self.session_maker() as session:
            return [self.entity_to_model(entity) for entity in
                    await session.execute(select(Entity).limit(limit).offset(offset))]

    @abstractmethod
    def entity_to_model(self, entity: Entity) -> Model:
        pass

    @abstractmethod
    def model_to_entity(self, model: Model) -> Entity:
        pass
