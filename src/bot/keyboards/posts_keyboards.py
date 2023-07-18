from aiogram import types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from sqlalchemy.orm import sessionmaker

from src.db.models.user import get_user


async def keyboards_for_post(message: types.Message, session_maker: sessionmaker) -> InlineKeyboardMarkup:
    posts_keyboards = InlineKeyboardBuilder()
    user = await get_user(message.from_user.id, session_maker)
    for post in user.posts:
        posts_keyboards.button(text=post.text[:20], callback_data=str(post.id))
    posts_keyboards.button(text='Создать пост', callback_data='createpost')
    posts_keyboards.adjust(1)
    return posts_keyboards.as_markup()


def cancel_create_post() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    return kb_builder.button(text='Отмена').as_markup(resize_keyboard=True)


def create_post_pr_type() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.button(text='Оплата за одну публикацию')
    kb_builder.button(text='Оплата за переход по ссылке')
    kb_builder.button(text='Отмена')
    kb_builder.adjust(1)
    return kb_builder.as_markup(resize_keyboard=True)
