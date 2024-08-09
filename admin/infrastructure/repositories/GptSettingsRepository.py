from abstractions.repositories.GptSettingsRepositoryInterface import GptSettingsRepositoryInterface
from domain.dto.gpt import GPTCreateDTO, GPTUpdateDTO
from domain.models import GPT as GPTModel
from infrastructure.entities import GPT
from infrastructure.repositories import AbstractSQLAlchemyRepository


class GPTRepository(
    AbstractSQLAlchemyRepository[
        GPT, GPTModel, GPTCreateDTO, GPTUpdateDTO
    ],
    GptSettingsRepositoryInterface,
):
    def entity_to_model(self, entity: GPT) -> GPTModel:
        return GPTModel(
            id=str(entity.id),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            model=entity.model,
            assistant=entity.assistant,
            token=entity.token,
            service_prompt=entity.service_prompt,
            proxy=entity.proxy,
        )

    def model_to_entity(self, model: GPTModel) -> GPT:
        return GPT(
            id=model.id,
            # created_at=model.created_at,
            # updated_at=model.updated_at,
            model=model.model,
            assistant=model.assistant,
            token=model.token,
            service_prompt=model.service_prompt,
            proxy=model.proxy,
        )
