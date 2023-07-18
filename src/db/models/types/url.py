import sqlalchemy.types as types


class URLTypeError(Exception):
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text


class URLType(types.TypeDecorator):
    impl = types.TEXT
    prefix = "URL:"

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

    def copy(self, **kw):
        return URLType()
