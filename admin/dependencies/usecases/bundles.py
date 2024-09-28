from abstractions.usecases.BundlesUserCaseInterface import BundlesUseCaseInterface
from dependencies.repositories.bundles import get_bundles_repository
from usecases.BundlesUseCase import BundlesUseCase


def get_bundles_use_case() -> BundlesUseCaseInterface:
    return BundlesUseCase(
        repository=get_bundles_repository(),
    )
