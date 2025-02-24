from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.repositories.sqlalchemy import session_maker


def get_session_maker() -> async_sessionmaker:
    return session_maker
