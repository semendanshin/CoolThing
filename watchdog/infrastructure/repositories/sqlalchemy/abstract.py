from abc import abstractmethod
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from abstractions.repositories import CRUDRepositoryInterface


@dataclass
class AbstractSQLAlchemyRepository[Entity, Model, CreateDTO, UpdateDTO](
    CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO]
):
    session_maker: async_sessionmaker

    async def create(self, obj: CreateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                session.add(self.model_to_entity(obj))

    async def get(self, obj_id: str) -> Model:
        actual_type = self.__orig_bases__[0].__args__[0]
        async with self.session_maker() as session:
            return self.entity_to_model(await session.get(actual_type, obj_id))

    async def update(self, obj: UpdateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await session.merge(self.model_to_entity(obj))

    async def delete(self, obj_id: str) -> None:
        actual_type = self.__orig_bases__[0].__args__[0]
        async with self.session_maker() as session:
            async with session.begin():
                await session.delete(await session.get(actual_type, obj_id))

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        actual_type = self.__orig_bases__[0].__args__[0]
        async with self.session_maker() as session:
            return [self.entity_to_model(entity) for entity in
                    await session.execute(select(actual_type).limit(limit).offset(offset))]

    @abstractmethod
    def entity_to_model(self, entity: Entity) -> Model:
        pass

    @abstractmethod
    def model_to_entity(self, model: Model) -> Entity:
        pass
