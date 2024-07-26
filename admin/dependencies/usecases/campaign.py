from abstractions.usecases.CampaingsUseCaseInterface import CampaignsUseCaseInterface
from usecases.mocks.MockCampaignsUseCase import MockCampaignsUseCase


def get_campaigns_usecase() -> CampaignsUseCaseInterface:
    return MockCampaignsUseCase()
