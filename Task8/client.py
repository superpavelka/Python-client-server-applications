"""Программа-клиент"""

import sys
import json
import socket
import time
import re
import logging
import threading
import logs.client_config
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError
from common.variables import ACTION, PRESENCE, TIME, USER, LOGIN, \
    RESPONSE, ERROR, DEFAULT_IP, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, \
    DESTINATION, EXIT
from common.utils import get_message, send_message
from decorators import log_extra_info

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log_extra_info
def create_exit_message(login):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        LOGIN: login
    }


@log_extra_info
def message_from_server(sock, login):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == login:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Получено сообщение от пользователя {message[SENDER]}:'
                                   f'\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            CLIENT_LOGGER.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            CLIENT_LOGGER.critical(f'Потеряно соединение с сервером.')
            break


@log_extra_info
def create_message(sock, login='Guest'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    receiver = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: login,
        DESTINATION: receiver,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение для пользователя {receiver}')
    except:
        CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log_extra_info
def user_interactive(sock, login):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, login)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(login))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


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
    print('Консольный месседжер. Клиентский модуль.')
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
    if '-n' in sys.argv:
        client_name = sys.argv[sys.argv.index('-n') + 1]
    else:
        client_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address} , порт: {server_port}, '
                       f'имя пользователя: {client_name}')
    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
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
        # запускаем клиенский процесс приёма сообщений
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        # Watchdog основной цикл, если один из потоков завершён,
        # то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках,
        # достаточно просто завершить цикл.
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
