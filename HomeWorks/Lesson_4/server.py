import socket
import click
import time
import select
from click.exceptions import UsageError
import json
import logging
import HomeWorks.Lesson_4.logs.config_server_log
from HomeWorks.Lesson_4.common.functions import *
from HomeWorks.Lesson_4.errors import IncorrectDataRecivedError
from HomeWorks.Lesson_4.decorators import log


server_logger = logging.getLogger('server')


# Обрабатываем сообщение клиента


@log
def proc_client_message(message, messages_list, client, clients, names):
    server_logger.debug(f'Обработка сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
        # Если такой пользователь ещё не зарегистрирован, регистрируем, иначе
        # отправляем ответ и завершаем соединение.
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не
        # требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    # Если клиент выходит
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[ACCOUNT_NAME])
        names[ACCOUNT_NAME].close()
        del names[ACCOUNT_NAME]
        return
    # Иначе отдаём Bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    """" Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение, список
    зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает."""
    if message[DESTINATION] in names and names[message[DESTINATION]
                                               ] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        server_logger.info(
            f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        server_logger.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, отправка сообщения невозможна.')


# Перехват оишибок, выдаваемых click при парсинге командной строки


def _show_usage_error(self):
    if '-p' in self.format_message():
        server_logger.critical(
            f'Попытка запуска сервера с некорректными параметрами порта. \n'
            f'После параметра -\'p\' необходимо указать номер порта и это должно быть целое число')
    elif '-a' in self.format_message():
        server_logger.critical(
            f'Попытка запуска сервера с некорректными параметрами адреса. \n'
            f'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')


UsageError.show = _show_usage_error


@click.command()
@click.option('-p', default=DEFAULT_PORT)
@click.option('-a', default='')
def start(p, a):
    listen_port = p
    if listen_port < 1024 or listen_port > 65535:
        server_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
            f'Допустимы адреса с 1024 до 65535.')
        exit(1)
    listen_address = a
    server_logger.info(
        f'Запущен сервер, порт для подключений: {listen_port} , адрес с которого '
        f'принимаются подключения: {listen_address}. Если адрес не указан, принимаются '
        f'соединения с любых адресов.')
    transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_socket.bind((listen_address, listen_port))
    transfer_socket.settimeout(0.5)

    clients = []
    messages = []
    names = dict()

    transfer_socket.listen(MAX_CONNECTED)

    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client, client_address = transfer_socket.accept()
        except OSError:
            pass
        else:
            server_logger.info(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(
                    clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения, кладём в словарь, если
        # ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    proc_client_message(
                        get_message(client_with_message),
                        messages,
                        client_with_message, clients, names)
                except ConnectionError:
                    server_logger.info(
                        f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

                # Если есть сообщения, обрабатываем каждое.
                for i in messages:
                    try:
                        process_message(i, names, send_data_lst)
                    except ConnectionError:
                        server_logger.info(
                            f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                        clients.remove(names[i[DESTINATION]])
                        del names[i[DESTINATION]]
                messages.clear()


if __name__ == '__main__':
    start()
