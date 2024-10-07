import logging
from dataclasses import dataclass

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO
from domain.models import ScriptForCampaign as ScriptForCampaignModel, ScriptMessage

logger = logging.getLogger(__name__)


@dataclass
class ScriptsUseCase(
    ScriptsUseCaseInterface,
):
    scripts_repository: ScriptsRepositoryInterface
    scripts_for_campaign_repository: ScriptsForCampaignRepositoryInterface

    async def get_active_scripts(self):
        pass

    async def get_scripts(self):
        scripts = await self.scripts_repository.get_all()
        return scripts

    async def get_script(self, script_id: str):
        script = await self.scripts_repository.get(obj_id=script_id)
        return script

    async def create_script(self, script_data: ScriptCreateDTO):
        await self.scripts_repository.create(obj=script_data)

    async def update_script(self, script_id: str, script_data: ScriptUpdateDTO):
        await self.scripts_repository.update(obj_id=script_id, obj=script_data)

    async def delete_script(self, script_id: str):
        await self.scripts_repository.delete(obj_id=script_id)

    async def start_script(self, script_id: str) -> list[ScriptMessage]:
        script = await self.scripts_repository.get(obj_id=script_id)
        return script.messages

    async def get_bots_mapping(self, script_id: str, campaign_id: str):
        return (await self.scripts_for_campaign_repository.get_by_complex_id(
            script_id=script_id,
            campaign_id=campaign_id
        )).bots_mapping

    async def get_active_script(self, sfc_id: str) -> ScriptForCampaignModel:
        return await self.scripts_for_campaign_repository.get(obj_id=sfc_id)

    async def sfc_done(self, sfc_id: str) -> None:
        await self.scripts_for_campaign_repository.sfc_done(sfc_id)