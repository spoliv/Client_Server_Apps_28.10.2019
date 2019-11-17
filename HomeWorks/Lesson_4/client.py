import socket
import time
import click
from click.exceptions import UsageError
import json
import logging
import HomeWorks.Lesson_4.logs.config_client_log
from HomeWorks.Lesson_4.errors import *
from HomeWorks.Lesson_4.common.functions import *
from HomeWorks.Lesson_4.decorators import log

client_logger = logging.getLogger('client')


# Формирование сообщения о присутствии


@log
def show_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    client_logger.debug(
        f'Сформировано {PRESENCE} сообщение от пользователя {account_name}')
    return out


# Обработка ответа сервера


@log
def proc_answer(message):
    client_logger.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


# Перехват оишибок, выдаваемых click при парсинге командной строки


def _show_usage_error(self):
    if '--port' in self.format_message():
        client_logger.critical(
            f'Попытка запуска клиента с некорректными параметрами порта сервера. \n'
            f'После параметра -\'port\' необходимо указать номер порта сервера и это должно быть целое число')
    elif '--addr' in self.format_message():
        client_logger.critical(
            f'Попытка запуска клиента с некорректными параметрами адреса сервера. \n'
            f'После параметра \'addr\'- необходимо указать адрес сервера')


UsageError.show = _show_usage_error


@click.command()
@click.option('--port', type=int, default=DEFAULT_PORT)
@click.option('--addr', default=DEFAULT_ADDRESS)
def start(port, addr):
    server_address = addr
    server_port = port
    if server_port < 1024 or server_port > 65535:
        client_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {server_port} сервера.'
            f'Допустимы адреса с 1024 до 65535.')
        exit(1)
    client_logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}')
    try:
        transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transfer_socket.connect((server_address, server_port))
        message_to_server = show_presence()
        send_message(transfer_socket, message_to_server)
        answer = proc_answer(get_message(transfer_socket))
        client_logger.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        client_logger.error(
            f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        client_logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг '
            f'запрос на подключение.')


if __name__ == '__main__':
    start()
