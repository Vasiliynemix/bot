from datetime import datetime

from aiogram.types import User, Chat, Message, CallbackQuery, Update

TEST_USER = User(id=1234, is_bot=False, first_name='Vasily', language_code='ru-RU', username='bot')

TEST_USER_CHAT = Chat(id=12, type='private', username=TEST_USER.username, first_name=TEST_USER.first_name)


def get_message(text: str):
    return Message(message_id=1234,
                   date=datetime.now(),
                   chat=TEST_USER_CHAT,
                   from_user=TEST_USER,
                   sender_chat=TEST_USER_CHAT,
                   text=text)


def get_update(message: Message = None, call: CallbackQuery = None):
    return Update(update_id=12345,
                  message=message if message else None,
                  callback_query=call if call else None)
