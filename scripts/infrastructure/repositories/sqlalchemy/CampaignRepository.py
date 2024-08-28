from abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from domain.dto.campaign import CampaignCreateDTO, CampaignUpdateDTO
from infrastructure.entities import Campaign
from infrastructure.repositories.sqlalchemy import AbstractSQLAlchemyRepository
from domain.models import Campaign as CampaignModel


class CampaignRepository(
    AbstractSQLAlchemyRepository[
        Campaign, CampaignModel, CampaignCreateDTO, CampaignUpdateDTO
    ],
    CampaignRepositoryInterface,
):
    def entity_to_model(self, entity: Campaign) -> CampaignModel:
        return CampaignModel(
            id=str(entity.id),
            welcome_message=entity.welcome_message,
            chats=entity.chats,
            plus_keywords=entity.plus_keywords,
            minus_keywords=entity.minus_keywords,
            gpt_settings_id=str(entity.gpt_settings_id),
            scope=entity.scope,
            new_lead_wait_interval_seconds=entity.new_lead_wait_interval_seconds,
            chat_answer_wait_interval_seconds=entity.chat_answer_wait_interval_seconds,
        )

    def model_to_entity(self, model: CampaignModel) -> Campaign:
        return Campaign(
            id=model.id,
            welcome_message=model.welcome_message,
            chats=model.chats,
            plus_keywords=model.plus_keywords,
            minus_keywords=model.minus_keywords,
            gpt_settings_id=model.gpt_settings_id,
            scope=model.scope,
            new_lead_wait_interval_seconds=model.new_lead_wait_interval_seconds,
            chat_answer_wait_interval_seconds=model.chat_answer_wait_interval_seconds,
        )
