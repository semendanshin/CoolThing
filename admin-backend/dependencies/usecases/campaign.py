from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from dependencies.repositories.campaign import get_campaign_repository
from usecases.CampaignsUseCase import CampaignsUseCase


def get_campaigns_usecase() -> CampaignsUseCaseInterface:
    return CampaignsUseCase(
        repository=get_campaign_repository()
    )
