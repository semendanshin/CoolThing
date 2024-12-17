from dataclasses import dataclass

from abstractions.repositories.campaign import CampaignRepositoryInterface
from abstractions.service.campaign import CampaignServiceInterface


@dataclass
class CampaignService(
    CampaignServiceInterface,
):
    campaign_repository: CampaignRepositoryInterface

    async def get_maximum_campaign_delay(self, campaign_id: str) -> int:
        campaign = await self.campaign_repository.get(campaign_id)
        return int(campaign.chat_answer_wait_interval_seconds.split('-')[1])  # TODO: check for type?
