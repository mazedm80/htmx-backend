from contextlib import asynccontextmanager
from typing import AsyncGenerator

from config.settings import settings
from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class PSQLHandler:
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
