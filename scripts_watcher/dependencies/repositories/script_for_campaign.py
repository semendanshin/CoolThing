from abstractions.repositories.script_for_campaign import ScriptsForCampaignRepositoryInterface
from infrastructure.repositories.beanie.script_for_campaign import ScriptsForCampaignRepository


def get_sfc_repository() -> ScriptsForCampaignRepositoryInterface:
    return ScriptsForCampaignRepository(

    )
