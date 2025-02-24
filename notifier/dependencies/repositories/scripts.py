from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from infrastructure.repositories.beanie.ScriptsForCampaignRepository import ScriptsForCampaignRepository
from infrastructure.repositories.beanie.ScriptsRepository import ScriptsRepository


def get_scripts_repository() -> ScriptsRepositoryInterface:
    return ScriptsRepository()


def get_script_for_campaign_repository() -> ScriptsForCampaignRepositoryInterface:
    return ScriptsForCampaignRepository()
