from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.dto.campaign import CampaignUpdateDTO
from domain.models import Campaign as CampaignModel


@dataclass
class CampaignsUseCaseInterface(ABC):
    @abstractmethod
    async def get_campaign(self, campaign_id: str) -> CampaignModel:
        ...

    @abstractmethod
    async def get_campaigns(self) -> list[CampaignModel]:
        ...

    @abstractmethod
    async def update_campaign(self, campaign_id: str, schema: CampaignUpdateDTO) -> list[CampaignModel]:
        ...
