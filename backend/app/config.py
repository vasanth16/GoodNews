from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    FETCH_INTERVAL_MINUTES: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
