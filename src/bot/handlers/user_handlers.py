from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from src.bot.handlers.create_post_handlers import menu_posts
from src.bot.keyboards.main_keyboard import create_main_keyboard
from src.bot.lexicon import MAIN_MENU_COMMANDS

router: Router = Router()


async def process_start_command(message: types.Message):
    return await message.answer(MAIN_MENU_COMMANDS['/start'],
                                reply_markup=create_main_keyboard())


async def process_help_command(message: types.Message):
    generate_help_message = ''
    for cmd, desc in MAIN_MENU_COMMANDS.items():
        generate_help_message += f'\n\n{cmd}\n{desc}'
    await message.answer(generate_help_message)


async def menu_channels(message: types.Message):
    await message.answer('Твои каналы')


async def menu_account(message: types.Message):
    await message.answer('Аккаунты')


def register_user_handlers(user_router: Router) -> None:
    user_router.message.register(process_start_command, CommandStart())
    user_router.message.register(process_help_command, Command(commands=['help']))

    user_router.message.register(menu_posts, F.text == 'Твои посты')

    user_router.message.register(menu_channels, F.text == 'Твои каналы')

    user_router.message.register(menu_account, F.text == 'Аккаунты')
