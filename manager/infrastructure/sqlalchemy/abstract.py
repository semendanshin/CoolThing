import asyncio
import logging
from abc import abstractmethod
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass
from typing import Callable, AsyncContextManager

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from abstractions.repositories import CRUDRepositoryInterface, UOWInterface

logger = logging.getLogger(__name__)


@dataclass
class AbstractSQLAlchemyRepository[Entity, Model, CreateDTO, UpdateDTO](
    CRUDRepositoryInterface[
        Model, CreateDTO, UpdateDTO
    ]
):
    session_maker: async_sessionmaker

    async def create(self, obj: CreateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                session.add(self.model_to_entity(obj))

    async def get(self, obj_id: str) -> Model:
        async with self.session_maker() as session:
            # noinspection PyUnresolvedReferences
            return self.entity_to_model(await session.get(self.__orig_bases__[0].__args__[0], obj_id))

    async def update(self, obj_id: str, obj: UpdateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                entity = await session.get(self.__orig_bases__[0].__args__[0], obj_id)
                for key, value in obj.__dict__.items():
                    setattr(entity, key, value)

    async def delete(self, obj_id: str) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                await session.delete(await session.get(Entity, obj_id))

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        entity = self.__orig_bases__[0].__args__[0]
        async with self.session_maker() as session:
            result = await session.execute(select(entity).limit(limit).offset(offset))
            return [self.entity_to_model(entity) for entity in
                    result.scalars().all()]

    @abstractmethod
    def entity_to_model(self, entity: Entity) -> Model:
        pass

    @abstractmethod
    def model_to_entity(self, model: Model) -> Entity:
        pass


@dataclass
class AbstractSQLAlchemyUOW(
    UOWInterface,
):
    session_maker: async_sessionmaker

    class FakeSession:
        def __init__(self, session):
            self._session = session

        async def close(self):
            pass

        async def commit(self):
            pass

        async def rollback(self):
            pass

        def begin(self):
            return self

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return False

        def __getattr__(self, item):
            try:
                return self._session.__getattribute__(item)
            except AttributeError:
                return self.__getattribute__(item)

    @classmethod
    def create_fake_session_maker(cls, session) -> Callable[[None], AsyncContextManager[AsyncSession]]:
        @asynccontextmanager
        async def session_maker():
            yield cls.FakeSession(session=session)

        return session_maker

    @asynccontextmanager
    async def begin(self, *repositories: AbstractSQLAlchemyRepository) -> 'AbstractSQLAlchemyUOW':
        async with self.session_maker() as session:
            async with session:
                async with session.begin():
                    session_maker = self.create_fake_session_maker(session)
                    for repository in repositories:
                        repository.session_maker = session_maker

                    yield self
