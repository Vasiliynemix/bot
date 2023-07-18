import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.bot.handlers.create_post_handlers import register_create_post_handlers
from src.bot.handlers.user_handlers import register_user_handlers
from src.bot.keyboards.main_menu import create_main_menu
from src.bot.middlewares.register_check import RegisterCheck
from src.bot.misc import redis
from src.configurations import conf
from src.db.database import create_async_engine, get_session_maker


async def bot_start(logger: logging.Logger):
    logging.basicConfig(level=logging.DEBUG)

    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)
    dp.message.middleware(RegisterCheck())

    bot = Bot(token=conf.bot.bot_token, parse_mode='HTML')

    await create_main_menu(bot)

    register_user_handlers(dp)
    register_create_post_handlers(dp)

    async_engine = create_async_engine(url=conf.db.build_connection_str())
    session_maker = get_session_maker(async_engine)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker, logger=logger, redis=redis)


def main():
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(bot_start(logger))
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')


if __name__ == '__main__':
    main()
