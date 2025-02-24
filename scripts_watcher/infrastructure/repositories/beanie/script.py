from uuid import UUID

from abstractions.repositories.script import ScriptsRepositoryInterface
from domain.models.script import Script as ScriptModel
from domain.models.script import ScriptMessage as ScriptMessageModel
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO
from infrastructure.entities.beanie import Script
from infrastructure.entities.beanie import Message as ScriptMessageEntity
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository


class ScriptsRepository(
    AbstractBeanieRepository[Script, ScriptModel, ScriptCreateDTO, ScriptUpdateDTO],
    ScriptsRepositoryInterface,
):

    def entity_to_model(self, entity: Script) -> ScriptModel:
        return ScriptModel(
            id=str(entity.id),
            name=entity.name,
            type=entity.type,
            messages=[ScriptMessageModel(bot_index=x.bot_index, text=x.text) for x in entity.messages],
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def model_to_entity(self, model: ScriptCreateDTO | ScriptModel) -> Script:
        if isinstance(model, ScriptModel):
            return Script(
                id=UUID(model.id),
                name=model.name,
                type=model.type,
                messages=[ScriptMessageEntity.model_validate(x) for x in model.messages],
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
        if isinstance(model, ScriptCreateDTO):
            return Script(
                id=model.id,
                name=model.name,
                type=model.type,
                messages=[ScriptMessageEntity(bot_index=int(x.bot.lstrip("bot")), text=x.text) for x in model.messages],
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
