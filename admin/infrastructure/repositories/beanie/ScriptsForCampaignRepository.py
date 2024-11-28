import logging
from datetime import datetime

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models import ScriptForCampaign as ScriptForCampaignModel
from infrastructure.entities import ScriptForCampaign
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository

logger = logging.getLogger(__name__)


class ScriptsForCampaignRepository(
    AbstractBeanieRepository[
        ScriptForCampaign, ScriptForCampaignModel, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ScriptsForCampaignRepositoryInterface,
):

    async def stop_active_script(self, sfc_id: str) -> bool:
        sfc = await self.entity.get(sfc_id)

        if sfc:
            sfc.stopped = True
            await sfc.save()
            return True

        logger.info(f"No sfc with id {sfc_id}")
        return False

    def update_model_to_entity(self, update_model: ScriptForCampaignUpdateDTO) -> ScriptForCampaign:
        return ScriptForCampaign(
            id=update_model.id,
            script_id=update_model.script_id,
            campaign_id=update_model.campaign_id,
            bots_mapping=update_model.bots_mapping,
            stopped=update_model.stopped,
        )

    def entity_to_model(self, entity: ScriptForCampaign) -> ScriptForCampaignModel:
        return ScriptForCampaignModel(
            id=str(entity.id),
            script_id=str(entity.script_id),
            campaign_id=str(entity.campaign_id),
            bots_mapping=entity.bots_mapping,
            done=entity.done,
            stopped=entity.stopped,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def model_to_entity(self, model: ScriptForCampaignCreateDTO | ScriptForCampaignModel) -> ScriptForCampaign:
        if isinstance(model, ScriptForCampaignModel):
            return ScriptForCampaign(
                id=model.id,
                script_id=model.script_id,
                campaign_id=model.campaign_id,
                bots_mapping=model.bots_mapping,
                done=model.done,
                stopped=model.stopped,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
        if isinstance(model, ScriptForCampaignCreateDTO):
            return ScriptForCampaign(
                id=model.id,
                script_id=model.script_id,
                campaign_id=model.campaign_id,
                bots_mapping=model.bots_mapping,
                done=False,
                stopped=False,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        raise TypeError("Unknown type to map into entity "
                        "(expected Union[`ScriptForCampaignModel`, `ScriptForCampaignCreateDTO`], "
                        f"got {type(model)})")
