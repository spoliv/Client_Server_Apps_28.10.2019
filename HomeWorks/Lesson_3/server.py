import socket
import click
import json
from HomeWorks.Lesson_3.common.functions import *


# Обрабатываем сообщение клиента


def proc_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message and \
            message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    else:
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }


@click.command()
@click.option('-p', type=int, default=DEFAULT_PORT)
@click.option('-a', default='')
def start(**kwargs):
    try:
        listen_port = kwargs['p']
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        exit(1)
    except ValueError:
        print(
            'В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)

    try:
        listen_address = kwargs['a']
    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        exit(1)

    transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transfer_socket.bind((listen_address, listen_port))

    transfer_socket.listen(MAX_CONNECTED)

    while True:
        client, client_address = transfer_socket.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            response = proc_client_message(message_from_cient)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    start()
