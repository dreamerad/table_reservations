import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Базовые настройки с значениями по умолчанию
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "restaurant_db"
    _POSTGRES_PASSWORD: str = "postgres"

    # Настройки приложения
    APP_NAME: str = "Restaurant Reservation API"
    API_PREFIX: str = ""

    # Настройки для тестирования
    TESTING: bool = False
    TEST_DATABASE_URL: str = "postgresql://postgres:postgres@localhost/test_restaurant_db"
    TEST_ASYNC_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost/test_restaurant_db"

    DB_ECHO: bool = False

    class Config:
        env_file = ".env"
        fields = {
            "_POSTGRES_PASSWORD": {"env": "POSTGRES_PASSWORD"}
        }

    @property
    def POSTGRES_PASSWORD(self) -> str:
        secret_path = '/run/secrets/postgres_password'
        if os.path.exists(secret_path):
            with open(secret_path, 'r') as f:
                return f.read().strip()

        return self._POSTGRES_PASSWORD

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()