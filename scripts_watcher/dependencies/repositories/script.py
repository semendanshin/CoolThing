from abstractions.repositories.script import ScriptsRepositoryInterface
from infrastructure.repositories.beanie.script import ScriptsRepository


def get_script_repository() -> ScriptsRepositoryInterface:
    return ScriptsRepository(

    )
