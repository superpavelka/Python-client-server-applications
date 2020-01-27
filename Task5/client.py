"""Программа-клиент"""

import sys
import json
import socket
import time
import re
import logging
import logs.client_config
from errors import ReqFieldMissingError
from common.variables import ACTION, PRESENCE, TIME, USER, LOGIN, \
    RESPONSE, ERROR, DEFAULT_IP, DEFAULT_PORT
from common.utils import get_message, send_message

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


def create_presence(login='Guest'):
    '''
    Функция генерирует запрос о присутствии клиента
    :param login:
    :return:
    '''
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            LOGIN: login
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {login}')
    return out


def process_ans(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK - Запрос выполнен успешно'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


def main():
    '''Загружаем параметы коммандной строки'''
    try:
        if '-a' in sys.argv:
            server_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_address = sys.argv[1]
        # Проверка IP адреса, если не соответсвует регулярке то выкинет исключение AttributeError
        [0 <= int(x) < 256 for x in
         re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', server_address).group(0))].count(True) == 4

        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = int(sys.argv[2])

        if server_port < 1024 or server_port > 65535:
            raise AttributeError

    except AttributeError:
        server_address = DEFAULT_IP
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта или IP адреса.'
            f'Установлены стандартные значения для '
            f'подключения {server_port},{server_address}')

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address} , порт: {server_port}')
    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        transport.connect((server_address, server_port))
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    message_to_server = create_presence()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{error.missing_field}')


if __name__ == '__main__':
    main()
