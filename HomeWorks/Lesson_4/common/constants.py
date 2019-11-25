import logging


DEFAULT_PORT = 7777
DEFAULT_ADDRESS = '127.0.0.1'
MAX_CONNECTED = 8
MAX_PACKAGE_SIZE = 1024
ENCODING = 'utf-8'
LOGGING_LEVEL = logging.DEBUG

# Ключи протокола JIM
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
SENDER = 'from'
DESTINATION = 'to'
EXIT = 'exit'


# Словари - ответы:
# 200
RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
