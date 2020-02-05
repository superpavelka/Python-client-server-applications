"""Программа-сервер"""

import socket
import sys
import re
import select
import logging
import logs.server_config
from common.variables import ACTION, LOGIN, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, DEFAULT_IP, MESSAGE, \
    MESSAGE_TEXT, SENDER, DESTINATION, EXIT
from common.utils import get_message, send_message
from decorators import log_extra_info

# Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log_extra_info
def process_client_message(message, messages_list, client, clients, names):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента
    '''
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    # Если это сообщение о присутствии, принимаем и отвечаем
    if ACTION in message and message[ACTION] == PRESENCE and \
            TIME in message and USER in message:
        # Если такой пользователь ещё не зарегистрирован,
        # регистрируем, иначе отправляем ответ и завершаем соединение.
        if message[USER][LOGIN] not in names.keys():
            names[message[USER][LOGIN]] = client
            send_message(client, {RESPONSE: 200})
        else:
            response = {RESPONSE: 400, ERROR: 'Имя пользователя уже занято!'}
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    # Если это сообщение, то добавляем его в очередь сообщений.
    # Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    # Если клиент выходит
    elif ACTION in message and message[ACTION] == EXIT and LOGIN in message:
        clients.remove(names[message[LOGIN]])
        names[message[LOGIN]].close()
        del names[message[LOGIN]]
        return
    # Иначе отдаём Bad request
    else:
        response = {RESPONSE: 400, ERROR: 'Запрос некорректен!'}
        send_message(client, response)
        return


@log_extra_info
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log_extra_info
def main():
    '''
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8000 -a 127.0.0.1
    '''
    # Проверяем порт
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

    # Проверяем адрес
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
    # словарь имен
    names = dict()
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
                                           messages, client_with_message, clients, names)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients.remove(client_with_message)

                # Если есть сообщения, обрабатываем каждое.
        for mes in messages:
            try:
                process_message(mes, names, send_data_lst)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем {mes[DESTINATION]} была потеряна')
            clients.remove(names[mes[DESTINATION]])
            del names[mes[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
