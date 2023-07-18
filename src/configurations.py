import logging
import os
import re
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import URL

load_dotenv()


@dataclass
class DbConfig:
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = int(os.getenv('DB_PORT'))

    DRIVER: str = "asyncpg"
    DB_SYSTEM: str = "postgresql"

    def build_connection_str(self) -> str:
        return URL.create(drivername=f'{self.DB_SYSTEM}+{self.DRIVER}',
                          username=self.DB_USER,
                          database=self.DB_NAME,
                          password=self.DB_PASS,
                          port=self.DB_PORT,
                          host=self.DB_HOST).render_as_string(hide_password=False)


@dataclass
class BotConfig:
    bot_token: str = os.getenv('BOT_TOKEN')


@dataclass
class Configuration:
    logging_level: int = int(os.getenv('LOGGING_LEVEL', logging.INFO))
    debug: bool = bool(os.getenv('DEBUG'))

    db: DbConfig = DbConfig()
    bot: BotConfig = BotConfig()


conf = Configuration()

