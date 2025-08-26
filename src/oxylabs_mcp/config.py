from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Project settings."""

    OXYLABS_SCRAPER_URL: str = "https://realtime.oxylabs.io/v1/queries"
    OXYLABS_REQUEST_TIMEOUT_S: int = 100
    LOG_LEVEL: str = "INFO"

    MCP_TRANSPORT: Literal["stdio", "sse", "streamable-http"] = "stdio"
    MCP_PORT: int = 8000
    MCP_HOST: str = "localhost"


settings = Settings()
