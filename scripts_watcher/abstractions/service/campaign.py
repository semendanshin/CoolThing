from abc import ABC, abstractmethod


class CampaignServiceInterface(ABC):
    @abstractmethod
    async def get_maximum_campaign_delay(self, campaign_id: str) -> int:
        ...
