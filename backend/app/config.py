from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central place for all environment-driven config.
    pydantic-settings reads these from the process environment / .env file
    automatically, so nothing here should be hardcoded.
    """

    groq_api_key: str
    groq_model: str = "gemma2-9b-it"
    database_url: str
    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
