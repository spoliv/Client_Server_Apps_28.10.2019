import socket
import click
from click.exceptions import UsageError
import json
import logging
import HomeWorks.Lesson_4.logs.config_server_log
from HomeWorks.Lesson_4.common.functions import *
from HomeWorks.Lesson_4.errors import IncorrectDataRecivedError


server_logger = logging.getLogger('server')


""" Обрабатываем сообщение клиента """


def proc_client_message(message):
    server_logger.debug(f'Обработка сообщения от клиента: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and \
            message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    else:
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


""" Перехват оишибок, выдаваемых click при парсинге командной строки """


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

    transfer_socket.listen(MAX_CONNECTED)

    while True:
        client, client_address = transfer_socket.accept()
        server_logger.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_cient = get_message(client)
            server_logger.debug(f'Получено сообщение {message_from_cient}')
            response = proc_client_message(message_from_cient)
            server_logger.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            server_logger.debug(
                f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            server_logger.error(
                f'Не удалось декодировать Json строку, полученную от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            server_logger.error(
                f'От клиента {client_address} приняты некорректные данные. Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    start()
