import enum
import logging
import sys
from dataclasses import dataclass
from os import getenv

from sqlalchemy.engine import URL

from src.db.enums import Role


class DatabaseType(str, enum.Enum):
    POSTGRES = "POSTGRES"
    SQLITE3 = "SQLITE3"


@dataclass
class DatabaseConfig:
    """Database connection variables."""

    db_type: DatabaseType = getenv("DB_TYPE", DatabaseType.SQLITE3)
    name: str = getenv('DB_NAME', "db")
    user: str | None = getenv('DB_USER')
    password: str | None = getenv("DB_PASSWORD")
    host: str | None = getenv('DB_HOST')
    port: int | None = int(getenv("DB_PORT"))

    # driver: str = 'aiosqlite'
    # database_system: str = 'sqlite'

    def build_connection_str(self) -> str:
        """This function build a connection string."""
        data = {
            DatabaseType.SQLITE3: self.__generate_sqllite_connection,
            DatabaseType.POSTGRES: self.__generate_postgres_connection
        }
        return data[self.db_type]()

    def __generate_postgres_connection(self) -> str:
        driver: str = 'asyncpg'
        database_system: str = 'postgresql'
        return URL.create(
            drivername=f'{database_system}+{driver}',
            username=self.user,
            database=self.name,
            password=self.password,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)

    def __generate_sqllite_connection(self) -> str:
        database_system: str = 'sqlite'
        driver: str = 'aiosqlite'
        return URL.create(
            drivername=f'{database_system}+{driver}',
            database=f'./data/{self.name}.db'
        ).render_as_string(hide_password=False)


@dataclass
class BotConfig:
    """Bot configuration."""

    token: str | None = getenv('BOT_TOKEN', None)


@dataclass
class RedisConfig:
    """Redis connection variables."""

    db: int = int(getenv('REDIS_DATABASE', 1))
    """ Redis Database ID """
    host: str = getenv('REDIS_HOST', 'localhost')
    port: int = int(getenv('REDIS_PORT', 6379))
    passwd: str | None = getenv('REDIS_PASSWORD')
    username: str | None = getenv('REDIS_USERNAME')
    state_ttl: int | None = getenv('REDIS_TTL_STATE', None)
    data_ttl: int | None = getenv('REDIS_TTL_DATA', None)


@dataclass
class LoggingConfig:
    logging_level: int = int(getenv("LOGGING_LEVEL", default=20))

    def get_basic_logging(self) -> logging.basicConfig:
        return logging.basicConfig(
            level=self.logging_level,
            format="%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s",
            stream=sys.stdout
        )

    def is_debug(self) -> bool:
        return self.logging_level == logging.DEBUG


@dataclass
class AdminsConfig:

    def get_admins(self) -> list[int] | None:
        admins = getenv('ADMINS')
        if ',' in admins:
            return [int(admin.strip()) for admin in admins.split(',')]
        return [int(admins.strip())]

    def get_role(self, user_id: int) -> Role:
        admins = self.get_admins()
        if user_id in admins:
            return Role.ADMINISTRATOR
        return Role.USER


@dataclass
class Configuration:
    db = DatabaseConfig()
    log = LoggingConfig()
    bot = BotConfig()
    redis = RedisConfig()
    admins = AdminsConfig()


conf = Configuration()
