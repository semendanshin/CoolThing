from abc import ABC

from abstractions.repositories import CRUDRepositoryInterface
from domain.dto.script import ScriptCreateDTO, ScriptUpdateDTO
from domain.models.script import Script


class ScriptsRepositoryInterface(
    CRUDRepositoryInterface[
        Script, ScriptCreateDTO, ScriptUpdateDTO,
    ],
    ABC,
):
    ...
