from abc import ABC, abstractmethod

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models import ScriptForCampaign


class ScriptsForCampaignRepositoryInterface(
    CRUDRepositoryInterface[
        ScriptForCampaign, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ABC,
):
    @abstractmethod
    async def get_by_complex_id(self, script_id: str, campaign_id: str) -> ScriptForCampaign:
        ...

    @abstractmethod
    async def sfc_done(self, sfc_id: str) -> None:
        ...

    @abstractmethod
    async def get_grouped_scripts_by_campaign(self) -> list:
        ...

    @abstractmethod
    async def get_grouped_scripts_by_bots(self) -> list:
        ...

    @abstractmethod
    async def get_grouped_scripts_by_chats(self) -> list:
        ...

    @abstractmethod
    async def get_chats_statistics_by_n_last_days(self, n: int) -> list:
        ...
