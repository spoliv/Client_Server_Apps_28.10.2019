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

# Функция - обработчик сообщений других пользователей, поступающих с сервера.
@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(
            f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        client_logger.info(
            f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        client_logger.error(
            f'Получено некорректное сообщение с сервера: {message}')


@log
# Функция запрашивает текст сообщения и возвращает его. Так же завершает
# работу при вводе подобной комманды
def create_message(sock, account_name='Guest'):
    message = input(
        'Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        client_logger.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict

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
@click.option('--mode', '-m', default='listen')
def start(port, addr, mode):
    server_address = addr
    server_port = port
    client_mode = mode
    if server_port < 1024 or server_port > 65535:
        client_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {server_port} сервера.'
            f'Допустимы адреса с 1024 до 65535.')
        exit(1)
    elif client_mode not in ('listen', 'send'):
        client_logger.critical(
            f'Указан недопустимый режим работы {client_mode}, допустимые режимы: listen , send')
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
        exit(1)
    except ReqFieldMissingError as missing_error:
        client_logger.error(
            f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except ConnectionRefusedError:
        client_logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг '
            f'запрос на подключение.')
        exit(1)
    else:
        # Если соединение с сервером установлено корректно, начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(
                        transfer_socket,
                        create_message(transfer_socket))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(
                        f'Соединение с сервером {server_address} было потеряно.')
                    exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transfer_socket))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    client_logger.error(
                        f'Соединение с сервером {server_address} было потеряно.')
                    exit(1)


if __name__ == '__main__':
    start()
