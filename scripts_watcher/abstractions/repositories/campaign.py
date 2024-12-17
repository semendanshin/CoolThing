from abc import ABC

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.campaign import CampaignCreateDTO, CampaignUpdateDTO
from domain.models.campaign import Campaign


class CampaignRepositoryInterface(
    CRUDRepositoryInterface[Campaign, CampaignCreateDTO, CampaignUpdateDTO],
    ABC,
):
    ...
