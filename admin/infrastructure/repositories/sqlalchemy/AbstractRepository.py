from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import joinedload

from abstractions.repositories import CRUDRepositoryInterface


@dataclass
class AbstractSQLAlchemyRepository[Entity, Model, CreateDTO, UpdateDTO](
    CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO]
):
    session_maker: async_sessionmaker

    options: list = field(default_factory=list)

    def __post_init__(self):
        self.entity: Type[Entity] = self.__orig_bases__[0].__args__[0]

    def _set_lazy_fields(self, fields: list[str]):
        self.options = [joinedload(getattr(self.entity, field)) for field in fields]

    async def create(self, obj: CreateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                session.add(self.model_to_entity(obj))

    async def get(self, obj_id: str) -> Model:
        async with self.session_maker() as session:
            if self.options:
                res = await session.execute(
                    select(self.entity)
                    .where(
                        self.entity.id == obj_id,
                        self.entity.deleted_at.is_(None)
                    )
                    .options(*self.options)
                )
            else:
                res = await session.execute(
                    select(self.entity)
                    .where(
                        self.entity.id == obj_id,
                        self.entity.deleted_at.is_(None)
                    )
                )
            obj = res.unique().scalars().one()
            return self.entity_to_model(obj)

    async def update(self, obj_id: str, obj: UpdateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                entity = await session.get(self.entity, obj_id)
                for key, value in obj.__dict__.items():
                    setattr(entity, key, value)

    async def delete(self, obj_id: str) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                obj = await session.get(self.entity, obj_id)
                obj.soft_delete()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        async with self.session_maker() as session:
            if self.options:
                return [
                    self.entity_to_model(entity)
                    for entity in (await session.execute(
                        select(self.entity)
                        .options(*self.options)
                        .where(self.entity.deleted_at.is_(None))
                        .limit(limit)
                        .offset(offset)
                    )).unique().scalars().all()
                ]
            else:
                return [
                    self.entity_to_model(entity)
                    for entity in (await session.execute(
                        select(self.entity)
                        .where(self.entity.deleted_at.is_(None))
                        .limit(limit)
                        .offset(offset)
                    )).scalars().all()
                ]

    @abstractmethod
    def entity_to_model(self, entity: Entity) -> Model:
        pass

    @abstractmethod
    def model_to_entity(self, model: Model) -> Entity:
        pass
