from abc import ABC, abstractmethod


class CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO](ABC):
    @abstractmethod
    async def create(self, obj: CreateDTO) -> None:
        pass

    @abstractmethod
    async def get(self, obj_id: str) -> Model:
        pass

    @abstractmethod
    async def update(self, obj_id: str, obj: UpdateDTO) -> None:
        pass

    @abstractmethod
    async def delete(self, obj_id: str) -> None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        pass
