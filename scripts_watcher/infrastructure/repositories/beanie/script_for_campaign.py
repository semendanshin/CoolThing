import logging
from datetime import datetime

from abstractions.repositories.script_for_campaign import ScriptsForCampaignRepositoryInterface
from domain.dto.script import ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
from domain.models.script import ScriptForCampaign as ScriptForCampaignModel
from infrastructure.entities.beanie import ScriptForCampaign
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository
from infrastructure.repositories.beanie.exceptions import NoSuchEntityException

logger = logging.getLogger(__name__)


class ScriptsForCampaignRepository(
    AbstractBeanieRepository[
        ScriptForCampaign, ScriptForCampaignModel, ScriptForCampaignCreateDTO, ScriptForCampaignUpdateDTO
    ],
    ScriptsForCampaignRepositoryInterface,
):

    async def sfc_done(self, sfc_id: str) -> None:
        sfc = await self.entity.get(sfc_id)

        if sfc:
            sfc.done = True
            await sfc.save()
            return

        logger.info(f"No sfc with id {sfc_id}")

    def entity_to_model(self, entity: ScriptForCampaign) -> ScriptForCampaignModel:
        return ScriptForCampaignModel(
            id=str(entity.id),
            script_id=str(entity.script_id),
            campaign_id=str(entity.campaign_id),
            bots_mapping=entity.bots_mapping,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            done=entity.done,
            stopped=entity.stopped,
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
                done=model.done,
            )
        if isinstance(model, ScriptForCampaignCreateDTO):
            return ScriptForCampaign(
                id=model.id,
                script_id=model.script_id,
                campaign_id=model.campaign_id,
                bots_mapping=model.bots_mapping,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                done=model.done,
            )
        raise TypeError("Unknown type to map into entity "
                        "(expected Union[`ScriptForCampaignModel`, `ScriptForCampaignCreateDTO`], "
                        f"got {type(model)})")

    async def get_by_complex_id(self, script_id: str, campaign_id: str) -> ScriptForCampaignModel:
        res = await self.entity.find(
            self.entity.script_id == script_id,
            self.entity.campaign_id == campaign_id,
            not self.entity.done,
        ).first_or_none()

        if res:
            return ScriptForCampaignModel(**res.model_dump())

        raise NoSuchEntityException
