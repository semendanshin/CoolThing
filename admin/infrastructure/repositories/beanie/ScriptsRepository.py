from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from domain.models import Script as ScriptModel
from domain.models import ScriptMessage as ScriptMessageModel
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO
from infrastructure.entities import Script
from infrastructure.entities import ScriptMessage as ScriptMessageEntity
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository


class ScriptsRepository(
    AbstractBeanieRepository[Script, ScriptModel, ScriptCreateDTO, ScriptUpdateDTO],
    ScriptsRepositoryInterface,
):

    def update_model_to_entity(self, update_model: ScriptUpdateDTO) -> Script:
        return Script(
            id=update_model.id,
            name=update_model.name,
            type=update_model.type,
            messages=[ScriptMessageEntity(bot_index=int(x.bot.lstrip("bot")), text=x.text) for x in update_model.messages],
        )

    def entity_to_model(self, entity: Script) -> ScriptModel:
        return ScriptModel(
            id=str(entity.id),
            name=entity.name,
            type=entity.type,
            messages=[ScriptMessageModel(bot_index=x.bot_index, text=x.text) for x in entity.messages],
        )

    def model_to_entity(self, model: ScriptCreateDTO | ScriptModel) -> Script:
        if isinstance(model, ScriptModel):
            return Script(
                id=model.id,
                name=model.name,
                type=model.type,
                messages=[ScriptMessageEntity.model_validate(x) for x in model.messages],
            )
        if isinstance(model, ScriptCreateDTO):
            return Script(
                id=model.id,
                name=model.name,
                type=model.type,
                messages=[ScriptMessageEntity(bot_index=int(x.bot.lstrip("bot")), text=x.text) for x in model.messages],
            )
