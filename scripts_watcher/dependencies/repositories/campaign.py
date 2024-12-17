from abstractions.repositories.campaign import CampaignRepositoryInterface
from dependencies.repositories import get_session_maker
from infrastructure.repositories.sqlalchemy.CampaignRepository import CampaignRepository


def get_campaign_repository() -> CampaignRepositoryInterface:
    return CampaignRepository(
        session_maker=get_session_maker(),
    )
