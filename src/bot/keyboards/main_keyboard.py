from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_main_keyboard() -> ReplyKeyboardMarkup:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text='Твои посты')
    menu_builder.button(text='Твои каналы')
    menu_builder.button(text='Аккаунты')
    return menu_builder.as_markup(resize_keyboard=True)
