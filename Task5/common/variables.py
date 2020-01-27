"""Константы"""

import logging

# Порт поумолчанию для сетевого ваимодействия
DEFAULT_PORT = 8000
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.INFO

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
LOGIN = 'login'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONSE_DEFAULT_IP = 'response_default_ip'
