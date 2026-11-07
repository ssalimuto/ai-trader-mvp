from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "ssalimuto bot"
    APP_SECRET_KEY: str
    JWT_SECRET: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./trades.db"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    ALLOWED_ORIGINS: str = "http://localhost:8000"
    UPDATE_PUBLIC_KEY_PATH: str = ""
    UPDATE_MANIFEST_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
