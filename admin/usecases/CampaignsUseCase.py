from dataclasses import dataclass

from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from domain.dto.campaign import CampaignUpdateDTO, CampaignCreateDTO
from domain.models import Campaign as CampaignModel


@dataclass
class CampaignsUseCase(
    CampaignsUseCaseInterface,
):
    repository: CampaignRepositoryInterface

    async def get_campaign(self, campaign_id: str) -> CampaignModel:
        return await self.repository.get(campaign_id)

    async def get_campaigns(self) -> list[CampaignModel]:
        return await self.repository.get_all()

    async def update(self, campaign_id: str, schema: CampaignUpdateDTO) -> list[CampaignModel]:
        await self.repository.update(campaign_id, schema)
        return await self.repository.get_all()

    async def create(self, schema: CampaignCreateDTO) -> None:
        return await self.repository.create(schema)

    async def delete(self, campaign_id: str) -> None:
        await self.repository.delete(campaign_id)
