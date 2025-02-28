import logging
from datetime import datetime, timedelta
from typing import List

from abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from domain.models import Script as ScriptModel
from domain.models import ScriptMessage as ScriptMessageModel
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO
from infrastructure.entities import Script
from infrastructure.entities import ScriptMessage as ScriptMessageEntity
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository

logger = logging.getLogger(__name__)

class ScriptsRepository(
    AbstractBeanieRepository[Script, ScriptModel, ScriptCreateDTO, ScriptUpdateDTO],
    ScriptsRepositoryInterface,
):
    async def get_scripts_by_n_last_days(self, n: int) -> List[ScriptModel]:
        threshold = datetime.now() - timedelta(days=n)
        logger.info("лол")
        logger.info(self.entity.__dict__)
        logger.info("тут")
        logger.info(await self.entity.find_all())
        logger.info("там")
        # Фильтруем по дате создания
        scripts = await self.entity.find(self.entity.created_at >= threshold).to_list()
        return [self.entity_to_model(script) for script in scripts]

    async def get_active_scripts(self, active_minutes: int = 15) -> List[ScriptModel]:
        threshold = datetime.now() - timedelta(minutes=active_minutes)
        # Здесь предполагается, что «активность» определяется по updated_at
        scripts = await self.entity.find(self.entity.updated_at >= threshold).to_list()
        return [self.entity_to_model(script) for script in scripts]

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
