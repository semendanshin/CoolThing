from dataclasses import dataclass

from abstractions.repositories.BundlesRepositoryInterface import BundlesRepositoryInterface
from abstractions.usecases.BundlesUserCaseInterface import BundlesUseCaseInterface
from domain.dto.bundle import BundleUpdateDTO, BundleCreateDTO
from domain.models import Bundle as BundleModel


@dataclass
class BundlesUseCase(
    BundlesUseCaseInterface,
):
    repository: BundlesRepositoryInterface

    async def get_campaign(self, bundle_id: str) -> BundleModel:
        return await self.repository.get(bundle_id)

    async def get_campaigns(self) -> list[BundleModel]:
        return await self.repository.get_all()

    async def update(self, bundle_id: str, schema: BundleUpdateDTO) -> list[BundleModel]:
        await self.repository.update(bundle_id, schema)
        return await self.repository.get_all()

    async def create(self, schema: BundleCreateDTO) -> None:
        return await self.repository.create(schema)

    async def delete(self, bundle_id: str) -> None:
        await self.repository.delete(bundle_id)

    async def add_worker_to_bundle(self, worker_id: str, bundle_id: str) -> None:
        await self.repository.add_worker_to_bundle(worker_id=worker_id, bundle_id=bundle_id)
