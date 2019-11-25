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
def proc_client_message(message, messages_list, client):
    server_logger.debug(f'Обработка сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and \
            message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
        # Если это сообщение, то добавляем его в очередь сообщений. Ответ не
        # требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
        # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


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
                        client_with_message)
                except BaseException:
                    server_logger.info(
                        f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им
        # сообщение.
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
                except BaseException:
                    server_logger.info(
                        f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients.remove(waiting_client)


if __name__ == '__main__':
    start()
