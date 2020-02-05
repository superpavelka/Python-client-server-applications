"""Программа-сервер"""

import socket
import sys
import re
import select
import logging
import time
import logs.server_config
from common.variables import ACTION, LOGIN, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decorators import log_extra_info

# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log_extra_info
def process_client_message(message, messages_list, client):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    '''
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][LOGIN] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[LOGIN], message[MESSAGE_TEXT]))
        return
    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Сервер не понимает запрос из-за неверного синтаксиса'
        })
        return


@log_extra_info
def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8000 -a 127.0.0.1
    :return:
    '''

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                   f'{listen_port}. Допустимы адреса с 1024 до 65535.')
            sys.exit(1)
    except IndexError:
        SERVER_LOGGER.critical(f'После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = DEFAULT_IP

    except IndexError:
        SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)
    # Проверка IP адреса, если не соответсвует регулярке то выкинет исключение AttributeError
    try:
        [0 <= int(x) < 256 for x in
         re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', listen_address).group(0))].count(True) == 4

    except AttributeError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего IP адреса '
                               f'{listen_address}.')
        sys.exit(1)

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}.')

    # Готовим сокет
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients = []
    messages = []

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)
    # Основной цикл программы сервера
    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с компьютером {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
