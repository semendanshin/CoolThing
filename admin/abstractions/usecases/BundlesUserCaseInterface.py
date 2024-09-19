from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.dto.bundle import BundleUpdateDTO, BundleCreateDTO
from domain.models import Bundle as BundleModel


@dataclass
class BundlesUseCaseInterface(ABC):
    @abstractmethod
    async def get_campaign(self, bundle_id: str) -> BundleModel:
        ...

    @abstractmethod
    async def get_campaigns(self) -> list[BundleModel]:
        ...

    @abstractmethod
    async def update(self, bundle_id: str, schema: BundleUpdateDTO) -> BundleModel:
        ...

    @abstractmethod
    async def create(self, schema: BundleCreateDTO) -> None:
        ...

    @abstractmethod
    async def delete(self, campaign_id: str) -> None:
        ...

    @abstractmethod
    async def add_worker_to_bundle(self, worker_id: str, bundle_id: str) -> None:
        ...
