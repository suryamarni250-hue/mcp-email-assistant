# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Tell pydantic-settings to use .env and ignore extra keys
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Email credentials (from your .env)
    EMAIL_ADDRESS: str = ""
    EMAIL_PASSWORD: str = ""

    # Email servers
    IMAP_HOST: str = "imap.gmail.com"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    # OAuth (for future use)
    OAUTH_CLIENT_ID: str = ""
    OAUTH_CLIENT_SECRET: str = ""

    # LLM
    OPENAI_API_KEY: str = ""

settings = Settings()
