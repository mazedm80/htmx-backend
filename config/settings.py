from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    """Schema for configuring API parameters."""

    host: str = "localhost"
    port: int = 3600
    debug: bool = False
    workers: int = 1

    class Config:
        env_prefix = "API_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = ApiSettings()
