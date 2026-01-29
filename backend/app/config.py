from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    FETCH_INTERVAL_HOURS: int = 24
    DATABASE_URL: str = "sqlite+aiosqlite:///./news.db"
    CORS_ORIGINS: str = "http://localhost:5173"
    LOG_LEVEL: str = "INFO"
    GEMINI_API_KEY: str = ""
    RATING_THRESHOLD: int = 65

    # News API sources
    GUARDIAN_API_KEY: str = ""
    GUARDIAN_ENABLED: bool = True
    THENEWSAPI_KEY: str = ""
    THENEWSAPI_ENABLED: bool = True

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS as comma-separated list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
