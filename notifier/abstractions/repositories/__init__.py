from abc import ABC, abstractmethod


class CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO](ABC):
    @abstractmethod
    async def create(self, obj: CreateDTO) -> None:
        ...

    @abstractmethod
    async def get(self, obj_id: str) -> Model:
        ...

    @abstractmethod
    async def update(self, obj_id: str, obj: UpdateDTO) -> None:
        ...

    @abstractmethod
    async def delete(self, obj_id: str) -> None:
        ...

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[Model]:
        ...


class UOWInterface(ABC):
    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    async def attach(self, *repositories: CRUDRepositoryInterface) -> None:
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...
