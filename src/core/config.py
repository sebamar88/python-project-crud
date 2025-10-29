from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_jwt_secret_key")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    class Config:
        env_file = ".env"


settings = Settings()
