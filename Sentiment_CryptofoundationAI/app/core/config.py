from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiment & Fear Intelligence API"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/hub_cf"

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # Auth
    INTERNAL_API_KEY: str = "super_secret_internal_key"

    # Fear Engine Weights
    WEIGHT_NEGATIVE_RATIO: float = 0.35
    WEIGHT_FEAR_PROB: float = 0.25
    WEIGHT_PANIC_KEYWORDS: float = 0.15
    WEIGHT_TREND_ACCELERATION: float = 0.15
    WEIGHT_VOLUME_SPIKE: float = 0.10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
