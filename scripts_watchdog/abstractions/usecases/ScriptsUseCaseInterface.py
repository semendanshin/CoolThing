from abc import ABC, abstractmethod

from domain.dto.script import ScriptUpdateDTO, ScriptCreateDTO
from domain.models import ScriptForCampaign as ScriptForCampaignModel, ScriptMessage


class ScriptsUseCaseInterface(ABC):
    @abstractmethod
    async def get_scripts(self):
        ...

    @abstractmethod
    async def get_script(self, script_id: str):
        ...

    @abstractmethod
    async def update_script(self, script_id: str, script_data: ScriptUpdateDTO):
        ...

    @abstractmethod
    async def delete_script(self, script_id: str):
        ...

    @abstractmethod
    async def create_script(self, script_data: ScriptCreateDTO):
        ...

    @abstractmethod
    async def start_script(self, script_id: str) -> list[ScriptMessage]:
        ...

    @abstractmethod
    async def get_bots_mapping(self, script_id: str, campaign_id: str) -> dict[str, str]:
        ...

    @abstractmethod
    async def get_active_scripts(self):
        ...

    @abstractmethod
    async def get_active_script(self, sfc_id: str) -> ScriptForCampaignModel:
        ...

    @abstractmethod
    async def sfc_done(self, sfc_id: str) -> None:
        ...

    @abstractmethod
    async def get_sfc_stop_status(self, sfc_id: str) -> bool:
        ...
