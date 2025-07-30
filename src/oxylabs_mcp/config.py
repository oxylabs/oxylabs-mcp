from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """Project settings."""

    OXYLABS_SCRAPER_URL: str = "https://realtime.oxylabs.io/v1/queries"
    OXYLABS_REQUEST_TIMEOUT_S: int = 100
    LOG_LEVEL: str = "INFO"


settings = Settings()
