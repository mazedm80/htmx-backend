from pydantic import BaseModel
from pydantic_settings import BaseSettings


class PSQL(BaseModel):
    """A class containing configuration parameters for connecting to a PostgreSQL database."""

    application_name: str = "htmx-fastapi"
    user: str = ""
    password: str = ""
    host: str = ""
    port: int = 5432
    database: str = ""
    max_connections: int = 4
    statement_timeout: float = 15.0

    def get_connection_url(self) -> str:
        """Returns the connection URL to establish an async connection to the PostgreSQL database."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class API(BaseModel):
    """Schema for configuring API parameters."""

    host: str = "localhost"
    port: int = 5000
    debug: bool = True
    workers: int = 1


class Settings(BaseSettings):
    """A class containing all the configuration parameters for the application."""

    api: API = API()
    psql: PSQL = PSQL()

    class Config:
        env_nested_delimiter = "__"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
