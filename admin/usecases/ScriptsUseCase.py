from dataclasses import dataclass

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from abstractions.usecases.EventsUseCaseInterface import EventsUseCaseInterface
from abstractions.usecases.ScriptsUseCaseInterface import ScriptsUseCaseInterface
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO, ScriptForCampaignCreateDTO
from domain.events.scripts import NewActiveScript


@dataclass
class ScriptsUseCase(
    ScriptsUseCaseInterface,
):
    scripts_repository: ScriptsRepositoryInterface
    scripts_for_campaign_repository: ScriptsForCampaignRepositoryInterface
    events_use_case: EventsUseCaseInterface

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
