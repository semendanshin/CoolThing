from abc import abstractmethod, ABC
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Type

from beanie import Document

from abstractions.repositories import CRUDRepositoryInterface


@dataclass
class AbstractBeanieRepository[Entity, Model, CreateDTO, UpdateDTO](
    CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO],
):
    def __post_init__(self):
        self.entity: Type[Entity] = self.__orig_bases__[0].__args__[0]

    async def create(self, obj: CreateDTO) -> None:
        instance: Document = self.model_to_entity(obj)
        await instance.create()

    async def get(self, obj_id: str) -> Model:
        instance = await self.entity.get(obj_id)
        return self.entity_to_model(instance)

    async def update(self, obj_id: str, obj: UpdateDTO) -> None:
        instance: Entity = await self.entity.get(obj_id)
        updated_instance: Entity = self.update_model_to_entity(obj)
        for key, value in updated_instance.model_dump().items():
            setattr(instance, key, value)

        instance.updated_at = datetime.now()

        await instance.save()

    async def delete(self, obj_id: str) -> None:
        instance = await self.entity.get(obj_id)
        await instance.delete()

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        instances = self.entity.find()
        res = []
        async for instance in instances:
            res.append(self.entity_to_model(instance))
        return res

    @abstractmethod
    def entity_to_model(self, entity: Entity) -> Model:
        ...

    @abstractmethod
    def model_to_entity(self, model: Model) -> Entity:
        ...

    @abstractmethod
    def update_model_to_entity(self, update_model: UpdateDTO) -> Entity:
        ...
