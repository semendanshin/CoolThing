from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.campaign import CampaignCreateDTO, CampaignUpdateDTO
from domain.models import Campaign


class CampaignRepositoryInterface(
    CRUDRepositoryInterface[
        Campaign, CampaignCreateDTO, CampaignUpdateDTO
    ],
    ABC,
):
    @abstractmethod
    async def get_campaign_names_by_ids(self, campaign_ids: list[str]) -> dict[str, str]:
        ...
