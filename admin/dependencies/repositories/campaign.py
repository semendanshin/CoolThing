from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from infrastructure.repositories.CampaignRepository import CampaignRepository
from . import get_session_maker


def get_campaign_repository() -> CampaignRepositoryInterface:
    return CampaignRepository(
        session_maker=get_session_maker(),
    )
