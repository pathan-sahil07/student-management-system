"""
Application configuration.

Centralizing settings here makes it easy to switch from in-memory storage
to a real database (e.g. SQLite) later without touching business logic.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Student Management System API"
    APP_VERSION: str = "1.0.0"

    # Toggle this (and implement database.py accordingly) to switch
    # from in-memory list storage to a persistent SQLite database.
    USE_DATABASE: bool = False
    DATABASE_URL: str = "sqlite:///./students.db"

    # Allowed origins for CORS - the Nuxt dev server runs on port 3000 by default.
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
