from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "DefaultApp"  # Add default values temporarily
    APP_VERSION: str = "1.0.0"
    OPENAI_API_KEY: str = "default-key"
    FILE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNK_SIZE:int

    class Config:
        env_file = env_file=".env",
        env_file_encoding = "utf-8"

def get_settings():
    settings = Settings()
    return settings