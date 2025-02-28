from abc import ABC, abstractmethod
from typing import List

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO
from domain.models import Script


class ScriptsRepositoryInterface(
    CRUDRepositoryInterface[
        Script, ScriptCreateDTO, ScriptUpdateDTO,
    ],
    ABC,
):
    @abstractmethod
    async def get_scripts_by_n_last_days(self, n: int) -> List[Script]:
        ...

    @abstractmethod
    async def get_active_scripts(self, active_minutes: int = 15) -> List[Script]:
        ...
