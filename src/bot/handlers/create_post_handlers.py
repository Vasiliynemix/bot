import os
import re

from aiogram import Router, Bot, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from src.bot.keyboards.main_keyboard import create_main_keyboard
from src.bot.keyboards.posts_keyboards import keyboards_for_post, cancel_create_post, create_post_pr_type
from src.db.models.post import PRType, create_post
from src.db.models.url import create_url

router: Router = Router()

bot = Bot(token=os.getenv('BOT_TOKEN'))

URL_CHECK = re.compile("^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}"
                       "\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$")


class PostStates(StatesGroup):
    waiting_for_select = State()
    waiting_for_text = State()
    waiting_for_url = State()
    waiting_for_budget = State()
    waiting_for_pr_type = State()
    waiting_for_price_url = State()
    waiting_for_price_publication = State()
    waiting_for_post_subs_min = State()


async def create_post_start(message: types.Message):
    await message.answer(text='Меню',
                         reply_markup=create_main_keyboard())


async def menu_posts(message: types.Message, session_maker: sessionmaker, state: FSMContext) -> None:
    await state.set_state(PostStates.waiting_for_select)
    await message.answer(text='Твои посты',
                         reply_markup=await keyboards_for_post(message=message, session_maker=session_maker))


async def menu_posts_create(call: types.CallbackQuery, state: FSMContext) -> None:
    """
        Создаем пост
    :param call:
    :param state:
    :return:
    """
    await call.message.answer('Отправь текст нового поста',
                              reply_markup=cancel_create_post())
    await bot.answer_callback_query(call.id)
    await state.set_state(PostStates.waiting_for_text)


async def menu_posts_create_text(message: types.Message, state: FSMContext) -> None:
    """
        Добавление текста для поста
    :param message:
    :param state:
    :return:
    """
    if message.text == 'Отмена':
        await state.clear()
        return await create_post_start(message)
    await state.update_data(post_text=message.text)
    await state.set_state(PostStates.waiting_for_url)
    await message.answer('Хорошо!\nТеперь отправь мне ссылку под постом.',
                         reply_markup=cancel_create_post())


async def menu_posts_create_url(message: types.Message, state: FSMContext):
    """
        Добавление ссылки для поста
    :param message:
    :param state:
    :return:
    """
    if message.text == 'Отмена':
        await state.clear()
        return await create_post_start(message)
    if URL_CHECK.match(message.text):
        await state.update_data(post_url=message.text)
        await state.set_state(PostStates.waiting_for_pr_type)
        await message.answer('Теперь выбери вариант раскрутки поста',
                             reply_markup=create_post_pr_type())
    else:
        await message.answer('Это не ссылка, отправьте ссылку!',
                             reply_markup=cancel_create_post())


async def menu_posts_create_pr_type(message: types.Message, state: FSMContext):
    """
        Добавление типа раскрутки
    :param message:
    :param state:
    :return:
    """
    match message.text:
        case 'Отмена':
            await state.clear()
            return await create_post_start(message)
        case 'Оплата за одну публикацию':
            await state.update_data(pr_type=PRType.PUBLICATIONS.value)
            await state.set_state(PostStates.waiting_for_price_publication)
            return await message.answer('отправь цену одной публикации',
                                        reply_markup=cancel_create_post())
        case 'Оплата за переход по ссылке':
            await state.update_data(pr_type=PRType.CLICKS.value)
            await state.set_state(PostStates.waiting_for_price_url)
            return await message.answer('отправь цену за один переход по ссылке (в руб)',
                                        reply_markup=cancel_create_post())
        case _:
            await message.answer('Выбери один из предложенных вариантов (в руб)',
                                 reply_markup=create_post_pr_type())


async def menu_posts_create_pr_type_url(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    """
        Получение цена за один переход по ссылке
    :param session_maker:
    :param message:
    :param state:
    :return:
    """
    price: float
    try:
        price = float(message.text)
        assert price > 0
        assert price <= 100
    except (TypeError, AssertionError):
        return await message.answer('Отправь цену в руб, Цена должна быть больше 0 и не меньше 100 руб.',
                                    reply_markup=cancel_create_post())
    data = await state.get_data()
    post = await create_post(
        session_maker=session_maker,
        text=data['post_text'],
        pr_type=PRType(data['pr_type']),
        author_id=message.from_user.id,
        url_price=price,
    )

    await create_url(session_maker, url_text=data['post_url'], post=post)

    await state.clear()
    await message.answer('Пост был создан')
    return await create_post_start(message, state=state)


async def menu_posts_create_pr_type_pub(message: types.Message, state: FSMContext):
    """
        Получение цена за один публикацию
    :param message:
    :param state:
    :return:
    """
    price: float
    try:
        price = float(message.text)
    except ValueError:
        return await message.answer('отправь цену в руб')
    await state.update_data(price=price)
    await state.set_state(PostStates.waiting_for_post_subs_min)
    await message.answer('Укажи минимальное количество подписчиков, которое требуется для публикации',
                         reply_markup=cancel_create_post())


async def menu_posts_create_subs_min(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    """

    :param message:
    :param state:
    :param session_maker:
    :return:
    """
    subs_min: int
    try:
        subs_min = int(message.text)
    except TypeError:
        return await message.answer('Отправь число подписчиков',
                                    reply_markup=cancel_create_post())
    data = await state.get_data()
    post = await create_post(session_maker=session_maker,
                             text=data['post_text'],
                             pr_type=PRType(data['pr_type']),
                             pub_price=data['price'],
                             subs_min=subs_min,
                             author_id=message.from_user.id,
                             url=data['post_url'])
    await state.clear()
    if post:
        await message.answer('Пост был успешно создан')
    else:
        await message.answer('В ходе создания произошла ошибка')
    return await create_post_start(message)


async def menu_posts_get(call: types.CallbackQuery) -> None:
    pass


def register_create_post_handlers(post_router: Router) -> None:
    post_router.message.register(menu_posts_create_text, PostStates.waiting_for_text)
    post_router.message.register(menu_posts_create_url, PostStates.waiting_for_url)
    post_router.message.register(menu_posts_create_pr_type, PostStates.waiting_for_pr_type)
    post_router.message.register(menu_posts_create_subs_min, PostStates.waiting_for_post_subs_min)
    post_router.message.register(menu_posts_create_pr_type_url, PostStates.waiting_for_price_url)
    post_router.message.register(menu_posts_create_pr_type_pub, PostStates.waiting_for_price_publication)

    post_router.callback_query.register(menu_posts_create, F.data == 'createpost', PostStates.waiting_for_select)

    post_router.message.register(menu_posts_get, F.data.startswith('getpost'), PostStates.waiting_for_select)
