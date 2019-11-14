import socket
import time
import click
import json
from HomeWorks.Lesson_3.common.functions import *


# Формирование сообщения о присутствии


def show_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out

# Обработка ответа сервера


def proc_answer(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        elif message[RESPONSE] == 400:
            return f'400 : {message[ERROR]}'
    raise ValueError


@click.command()
@click.option('--port', type=int, default=DEFAULT_PORT)
@click.option('--addr', default=DEFAULT_ADDRESS)
def start(**kwargs):
    try:
        server_address = kwargs['addr']
        server_port = kwargs['port']
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except KeyError:
        server_address = DEFAULT_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print(
            'В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)

    transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_socket.connect((server_address, server_port))
    message_to_server = show_presence()
    send_message(transfer_socket, message_to_server)
    try:
        answer = proc_answer(get_message(transfer_socket))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    start()
