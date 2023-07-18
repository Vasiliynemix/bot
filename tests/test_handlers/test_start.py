import pytest
from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage

from src.bot.keyboards.main_keyboard import create_main_keyboard
from src.bot.lexicon import MAIN_MENU_COMMANDS
from utils import get_update, get_message


@pytest.mark.asyncio
async def test_process_start_command(dispatcher: Dispatcher, bot: Bot):
    result = await dispatcher.feed_update(bot=bot, update=get_update(message=get_message(text='/start')))
    assert isinstance(result, SendMessage)
    assert result.text == MAIN_MENU_COMMANDS['/start']
    assert result.reply_markup == create_main_keyboard()
