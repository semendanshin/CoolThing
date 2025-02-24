from datetime import datetime
from uuid import UUID

from abstractions.repositories.active_script_process import ActiveScriptProcessRepositoryInterface
from domain.dto.script import ActiveScriptProcessCreateDTO, ActiveScriptProcessUpdateDTO
from domain.models import (
    ActiveScriptProcess as ActiveScriptProcessModel, ChatProcess,
)
from infrastructure.entities.beanie import ActiveScriptProcess
from infrastructure.repositories.beanie.AbstractRepository import AbstractBeanieRepository


class ActiveScriptProcessRepository(
    AbstractBeanieRepository[
        ActiveScriptProcess,
        ActiveScriptProcessModel,
        ActiveScriptProcessCreateDTO,
        ActiveScriptProcessUpdateDTO,
    ],
    ActiveScriptProcessRepositoryInterface,
):
    async def get_by_sfc(self, sfc_id: str) -> ActiveScriptProcessModel:
        print(sfc_id)
        return self.entity_to_model(await ActiveScriptProcess.find_one(ActiveScriptProcess.sfc_id == UUID(sfc_id)))

    def update_model_to_entity(self, update_model: ActiveScriptProcessUpdateDTO) -> ActiveScriptProcess:
        raise NotImplemented

    async def set_process(self, process_id: str, process: list[ChatProcess]):
        async with self._get_raw_entity(process_id) as process_entity:  # type: ActiveScriptProcess
            process_entity.process = process

    async def end_script(self, process_id: str, is_successful: bool, is_processed: bool):
        async with self._get_raw_entity(process_id) as process:  # type: ActiveScriptProcess
            if is_processed:
                process.processed_at = datetime.now()

            process.is_successful = is_successful

    async def end_chat(self, process_id: str, chat_link: str, is_successful: bool, is_processed: bool):
        async with self._get_raw_entity(process_id) as process:  # type: ActiveScriptProcess
            # find the only one needed chat
            chat: ChatProcess = list(filter(lambda x: x.chat_link == chat_link, process.process))[0]
            if is_processed:
                chat.processed_at = datetime.now()

            chat.is_successful = is_successful

            if not is_processed:
                for message in chat.messages:
                    if message.sent_at:
                        continue

                    message.will_be_sent = False

    async def end_message(self, process_id: str, message_id: str, send: bool, text: str = None):
        async with self._get_raw_entity(process_id) as process:  # type: ActiveScriptProcess
            for chat in process.process:
                for message in chat.messages:
                    if message.id != message_id:
                        continue

                    message.text = text
                    if send:
                        message.sent_at = datetime.now()

    async def set_target_chats(self, process_id: str, target_chats: list[str]):
        async with self._get_raw_entity(process_id) as process:  # type: ActiveScriptProcess
            process.target_chats = target_chats

    def entity_to_model(self, entity: ActiveScriptProcess) -> ActiveScriptProcessModel:
        return ActiveScriptProcessModel(
            id=str(entity.id),
            sfc_id=str(entity.sfc_id),
            target_chats=entity.target_chats,
            process=entity.process if entity.process else None,
            processed_at=entity.processed_at,
            is_successful=entity.is_successful,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def model_to_entity(self, model: ActiveScriptProcessCreateDTO | ActiveScriptProcessModel) -> ActiveScriptProcess:
        if isinstance(model, ActiveScriptProcessCreateDTO):
            return ActiveScriptProcess(
                id=model.id,
                sfc_id=UUID(model.sfc_id),
                target_chats=model.target_chats,
                process=model.process,
                processed_at=model.processed_at,
                is_successful=model.is_successful,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )

        raise Exception(
            "This was not intended to run. "
            "Check the sources in infrastructure/repositories/beanie/active_scripts_process.py"
        )
