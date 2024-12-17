from abc import ABC, abstractmethod
from uuid import UUID

from domain.dto.script import ScriptUpdateDTO, ScriptCreateDTO, ScriptForCampaignCreateDTO
from domain.models import ScriptForCampaign, ActiveScriptProcess


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
    async def activate_script(self, script: ScriptForCampaignCreateDTO):
        ...

    @abstractmethod
    async def stop_script(self, sfc_id: str) -> bool:
        ...

    @abstractmethod
    async def get_active_scripts(self) -> list[ScriptForCampaign]:
        ...

    @abstractmethod
    async def get_active_script(self, sfc_id: str) -> ActiveScriptProcess:
        ...

    @abstractmethod
    async def get_active_script_by_sfc(self, sfc_id: str) -> ActiveScriptProcess:
        ...

    @abstractmethod
    async def get_sfc(self, sfc_id: str) -> ScriptForCampaign:
        ...
