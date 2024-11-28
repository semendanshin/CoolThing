from datetime import datetime

from abstractions.repositories.ScriptsForCampaignRepositoryInterface import ScriptsForCampaignRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models import ScriptForCampaign as ScriptForCampaignModel
from infrastructure.entities.beanie import ScriptForCampaign
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository


class ScriptsForCampaignRepository(
    AbstractBeanieRepository[
        ScriptForCampaign, ScriptForCampaignModel, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ScriptsForCampaignRepositoryInterface,
):

    def update_model_to_entity(self, update_model: ScriptForCampaignUpdateDTO) -> ScriptForCampaign:
        return ScriptForCampaign(
            id=update_model.id,
            script_id=update_model.script_id,
            campaign_id=update_model.campaign_id,
            bots_mapping=update_model.bots_mapping,
        )

    def entity_to_model(self, entity: ScriptForCampaign) -> ScriptForCampaignModel:
        return ScriptForCampaignModel(
            id=str(entity.id),
            script_id=str(entity.script_id),
            campaign_id=str(entity.campaign_id),
            bots_mapping=entity.bots_mapping,
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
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        raise TypeError("Unknown type to map into entity "
                        "(expected Union[`ScriptForCampaignModel`, `ScriptForCampaignCreateDTO`], "
                        f"got {type(model)})")
