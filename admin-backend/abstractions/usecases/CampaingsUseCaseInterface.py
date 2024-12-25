from abc import abstractmethod, ABC
from dataclasses import dataclass

from domain.dto.campaign import CampaignUpdateDTO, CampaignCreateDTO
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
    async def update(self, campaign_id: str, schema: CampaignUpdateDTO) -> CampaignModel:
        ...

    @abstractmethod
    async def create(self, schema: CampaignCreateDTO) -> CampaignModel:
        ...

    @abstractmethod
    async def delete(self, campaign_id: str) -> None:
        ...
