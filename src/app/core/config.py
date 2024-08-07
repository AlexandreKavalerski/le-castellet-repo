import os
from enum import Enum
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path = os.path.join(current_file_dir, "..", "..", ".env")
load_dotenv(env_path)


class MySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


class OpenAISettings(MySettings):
    OPENAI_API_KEY: str | None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_TEXT_CHUNK_SIZE: int = 5000
    OPENAI_SUMMARY_LAST_TOKENS_SIZE: int = 2500


class SplunkSettings(MySettings):
    SPLUNK_URL: str = "http://localhost:8088/services/collector/event"
    SPLUNK_TOKEN: str | None
    SPLUNK_IS_ENABLED: bool = False

class WhisperSettings(MySettings):
    WHISPER_MODEL: str = "tiny"
    WHISPER_FP16_ENABLED: bool = False
    WHISPER_LANGUAGE: str = "portuguese"


class AppSettings(MySettings):
    APP_NAME: str = "Fast API app"
    APP_PORT: str | None
    TIER_NAME: str | None
    APP_DESCRIPTION: str | None
    APP_VERSION: str | None
    LICENSE_NAME: str | None
    CONTACT_NAME: str | None
    CONTACT_EMAIL: str | None
    IS_DEBUG_ENABLED: bool | None = False


class CryptSettings(MySettings):
    SECRET_KEY: str | None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class DatabaseSettings(MySettings):
    pass


class SQLiteSettings(DatabaseSettings):
    SQLITE_URI: str = "./sql_app.db"
    SQLITE_SYNC_PREFIX: str = "sqlite:///"
    SQLITE_ASYNC_PREFIX: str = "sqlite+aiosqlite:///"


class MySQLSettings(DatabaseSettings):
    MYSQL_USER: str = "username"
    MYSQL_PASSWORD: str = "password"
    MYSQL_ROOT_PASSWORD: str | None
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 5432
    MYSQL_DB: str = "dbname"
    MYSQL_SYNC_PREFIX: str = "mysql"
    MYSQL_ASYNC_PREFIX: str = "mysql+aiomysql"
    # MYSQL_URL: str | None = None
    # MYSQL_URI: str = (
    #     f"{MYSQL_ASYNC_PREFIX}://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}/{MYSQL_DB}"
    # )

    @property
    def MYSQL_URL(self) -> str:
        return str(
            URL.build(
                scheme=self.MYSQL_ASYNC_PREFIX,
                # host=self.MYSQL_SERVER,
                # port=3310,
                # TODO: replace with default port and host when running locally
                host="localhost",
                port=self.MYSQL_PORT,
                user=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                path=f"/{self.MYSQL_DB}",
                # query_string=self.db_query_string,
            )
        )


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "postgres"
    POSTGRES_SYNC_PREFIX: str = "postgresql://"
    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"
    POSTGRES_URI: str = (
        f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    POSTGRES_URL: str | None


class FirstUserSettings(MySettings):
    ADMIN_NAME: str = "admin"
    ADMIN_EMAIL: str = "admin@admin.com"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "!Ch4ng3Th1sP4ssW0rd!"


class TestSettings(MySettings):
    TEST_NAME: str = "Tester User"
    TEST_EMAIL: str = "test@tester.com"
    TEST_USERNAME: str = "testeruser"
    TEST_PASSWORD: str = "Str1ng$t"


class RedisCacheSettings(MySettings):
    REDIS_CACHE_HOST: str = "localhost"
    REDIS_CACHE_PORT: int = 6379
    REDIS_CACHE_URL: str = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"


class ClientSideCacheSettings(MySettings):
    CLIENT_CACHE_MAX_AGE: int = 60


class RedisQueueSettings(MySettings):
    REDIS_QUEUE_HOST: str = "localhost"
    REDIS_QUEUE_PORT: int = 6379


class RedisRateLimiterSettings(MySettings):
    REDIS_RATE_LIMIT_HOST: str = "localhost"
    REDIS_RATE_LIMIT_PORT: int = 6379
    REDIS_RATE_LIMIT_URL: str = (
        f"redis://{REDIS_RATE_LIMIT_HOST}:{REDIS_RATE_LIMIT_PORT}"
    )


class DefaultRateLimitSettings(MySettings):
    DEFAULT_RATE_LIMIT_LIMIT: int = 10
    DEFAULT_RATE_LIMIT_PERIOD: int = 3600


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(MySettings):
    ENVIRONMENT: EnvironmentOption = "local"


class Settings(
    AppSettings,
    OpenAISettings,
    WhisperSettings,
    SplunkSettings,
    MySQLSettings,
    CryptSettings,
    FirstUserSettings,
    TestSettings,
    RedisCacheSettings,
    ClientSideCacheSettings,
    RedisQueueSettings,
    RedisRateLimiterSettings,
    DefaultRateLimitSettings,
    EnvironmentSettings,
):
    pass


settings = Settings()
