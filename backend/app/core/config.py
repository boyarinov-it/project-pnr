from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Project PNR API"
    app_env: str = "local"
    backend_port: int = 8000
    database_url: str = "postgresql://postgres:admin@localhost:5432/pnr_db"

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
