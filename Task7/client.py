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
    RESPONSE, ERROR, DEFAULT_IP, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decorators import log_extra_info

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


@log_extra_info
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log_extra_info
def create_message(sock, login='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input('Введите сообщение для отправки или \'xxx\' для завершения работы: ')
    if message == 'xxx':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        LOGIN: login,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log_extra_info
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


@log_extra_info
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


@log_extra_info
def main():
    '''Загружаем параметы коммандной строки'''
    if '-a' in sys.argv:
        server_address = sys.argv[sys.argv.index('-a') + 1]
    else:
        server_address = DEFAULT_IP
        CLIENT_LOGGER.info(f'Не найден параметр -\'a\'.'
                           f'Установлено стандартное значение IP адреса: {server_address}')
    if '-p' in sys.argv:
        server_port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.info(f'Не найден параметр -\'p\'.'
                           f'Установлено стандартное значение порта: {server_port}')
    try:
        # Проверка IP адреса, если не соответсвует регулярке то выкинет исключение AttributeError
        [0 <= int(x) < 256 for x in
         re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', server_address).group(0))].count(True) == 4
        if server_port < 1024 or server_port > 65535:
            raise AttributeError

    except AttributeError:
        server_address = DEFAULT_IP
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта или IP адреса.'
            f'Установлены стандартные значения для '
            f'подключения {server_port},{server_address}')
    if '-m' in sys.argv:
        client_mode = sys.argv[sys.argv.index('-m') + 1]
    else:
        client_mode = 'listen'
    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address} , порт: {server_port}, режим работы: {client_mode}')
    # Инициализация сокета и обмен

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_ans(get_message(transport))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
