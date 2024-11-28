from . import get_session_maker
from infrastructure.repositories.sqlalchemy.WorkersRepository import SQLAlchemyWorkerRepository


def get_workers_repository() -> SQLAlchemyWorkerRepository:
    return SQLAlchemyWorkerRepository(
        session_maker=get_session_maker(),
    )
