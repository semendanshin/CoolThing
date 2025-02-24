from abstractions.service.campaign import CampaignServiceInterface
from dependencies.repositories.campaign import get_campaign_repository
from services.campaign import CampaignService


def get_campaign_service() -> CampaignServiceInterface:
    return CampaignService(
        campaign_repository=get_campaign_repository(),
    )
