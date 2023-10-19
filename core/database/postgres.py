from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings


class SingletonMeta(type):
    """Metaclass to provide a singleton"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class PSQLHandler(metaclass=SingletonMeta):
    def __init__(self) -> None:
        """Initialize asynchronous SQLAlchemy Engine using asyncpg driver."""
        self.configuration = settings.psql
        self.engine = create_async_engine(
            self.configuration.get_connection_url(),
            pool_size=self.configuration.max_connections,
            connect_args={
                "server_settings": {
                    "application_name": self.configuration.application_name
                },
                "command_timeout": self.configuration.statement_timeout,
            },
            pool_pre_ping=True,
        )
        self.session_maker = sessionmaker(bind=self.engine, class_=AsyncSession)

    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """A context manager that yields a new AsyncSession object for interacting with the database."""
        async with self.session_maker() as session:
            yield session
            session.expunge_all()

    async def execute(self, statement, *args, **kwargs) -> Result:
        """Execute an SQL statement against the database and return the result."""
        async with self.async_session() as session:
            result = await session.execute(statement, *args, **kwargs)
            return result

    async def execute_commit(self, statement, *args, **kwargs) -> Result:
        """Execute an SQL statement against the database and commit the result."""
        async with self.async_session() as session:
            result = await session.execute(statement, *args, **kwargs)
            await session.commit()
            return result

    async def scalars(self, statement, *args, **kwargs) -> Result:
        """Execute an SQL statement against the database and return the ORM object."""
        async with self.async_session() as session:
            result = await session.scalars(statement, *args, **kwargs)
            return result
