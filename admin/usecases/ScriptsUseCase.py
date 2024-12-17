from dataclasses import dataclass
from uuid import UUID

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from abstractions.repositories.active_script_process import ActiveScriptProcessRepositoryInterface
from abstractions.usecases.BrokerEventsUseCaseInterface import BrokerEventsUseCaseInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO, ScriptForCampaignCreateDTO
from domain.events.broker.scripts import NewActiveScript
from domain.models import ScriptForCampaign, ActiveScriptProcess


@dataclass
class ScriptsUseCase(
    ScriptsUseCaseInterface,
):
    async def get_sfc(self, sfc_id: str) -> ScriptForCampaign:
        return await self.scripts_for_campaign_repository.get(sfc_id)

    async def get_active_script(self, process_id: str) -> ActiveScriptProcess:
        return await self.script_process_repository.get(obj_id=process_id)

    async def get_active_script_by_sfc(self, sfc_id: str) -> ActiveScriptProcess:
        return await self.script_process_repository.get_by_sfc(sfc_id)

    async def get_active_scripts(self) -> list[ScriptForCampaign]:
        return await self.scripts_for_campaign_repository.get_all()

    scripts_repository: ScriptsRepositoryInterface
    scripts_for_campaign_repository: ScriptsForCampaignRepositoryInterface
    script_process_repository: ActiveScriptProcessRepositoryInterface
    events_use_case: BrokerEventsUseCaseInterface

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

    async def activate_script(self, script: ScriptForCampaignCreateDTO):
        await self.scripts_for_campaign_repository.create(obj=script)
        event = NewActiveScript(
            script_for_campaign_id=script.id,
        )
        await self.events_use_case.publish(event)
        print(script.__dict__)
        print(event.__dict__)

    async def stop_script(self, sfc_id: str) -> bool:
        return await self.scripts_for_campaign_repository.stop_active_script(sfc_id=sfc_id)
