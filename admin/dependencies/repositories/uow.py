from abstractions.repositories import UOWInterface
from dependencies.repositories import get_session_maker
from infrastructure.repositories import AbstractSQLAlchemyUOW


def get_uow() -> UOWInterface:
    return AbstractSQLAlchemyUOW(
        session_maker=get_session_maker(),
    )
