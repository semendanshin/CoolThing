from abstractions.repositories.BundlesRepositoryInterface import BundlesRepositoryInterface
from infrastructure.repositories.sqlalchemy.BundlesRepository import BundlesRepository
from . import get_session_maker


def get_campaign_repository() -> BundlesRepositoryInterface:
    return BundlesRepository(
        session_maker=get_session_maker(),
    )
