from aiogram import Bot
from aiogram.types import BotCommand

from src.bot.lexicon import MAIN_MENU_COMMANDS


async def create_main_menu(bot: Bot):
    commands_for_bot = [BotCommand(command=cmd,
                                   description=desc)
                        for cmd, desc in MAIN_MENU_COMMANDS.items()]

    await bot.set_my_commands(commands=commands_for_bot)
