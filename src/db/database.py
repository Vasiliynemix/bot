from typing import AsyncGenerator

from sqlalchemy import MetaData, URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.configurations import conf

metadata = MetaData()


async def async_engine(url: URL | str) -> None:
    engine = create_async_engine(url=url, echo=True, pool_pre_ping=True)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
