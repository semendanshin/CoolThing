from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from domain.dto.campaign import CampaignCreateDTO, CampaignUpdateDTO
from infrastructure.entities import Campaign
from infrastructure.repositories import AbstractSQLAlchemyRepository
from domain.models import Campaign as CampaignModel


class CampaignRepository(
    AbstractSQLAlchemyRepository[
        Campaign, CampaignModel, CampaignCreateDTO, CampaignUpdateDTO
    ],
    CampaignRepositoryInterface,
):
    def entity_to_model(self, entity: Campaign) -> CampaignModel:
        return CampaignModel(
            id=entity.id,
            welcome_message=entity.welcome_message,
            chats=entity.chats,
            plus_keywords=entity.plus_keywords,
            minus_keywords=entity.minus_keywords,
            gpt_settings_id=entity.gpt_settings_id,
            topic=entity.topic,
            scope=entity.scope,
        )

    def model_to_entity(self, model: CampaignModel) -> Campaign:
        return CampaignModel(
            id=model.id,
            welcome_message=model.welcome_message,
            chats=model.chats,
            plus_keywords=model.plus_keywords,
            minus_keywords=model.minus_keywords,
            gpt_settings_id=model.gpt_settings_id,
            topic=model.topic,
            scope=model.scope,
        )