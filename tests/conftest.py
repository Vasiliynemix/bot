import asyncio

import pytest
import pytest_asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from mocked_bot import MockedBot
from src.bot.handlers.user_handlers import register_user_handlers


@pytest_asyncio.fixture(scope='session')
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture()
def bot():
    bot = MockedBot()
    token = Bot.set_current(bot)
    try:
        yield bot
    finally:
        Bot.reset_current(token)


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    register_user_handlers(dp)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()
