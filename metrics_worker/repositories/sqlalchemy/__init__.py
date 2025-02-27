from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings
from .AbstractRepository import AbstractSQLAlchemyRepository
from .AbstractUOW import AbstractSQLAlchemyUOW

__all__ = [
    "AbstractSQLAlchemyRepository",
    "AbstractSQLAlchemyUOW",
    "session_maker",
]

engine = create_async_engine(settings.db.url, echo=False)
session_maker = async_sessionmaker(engine, expire_on_commit=False)
