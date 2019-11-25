import socket
import time
import click
import threading
from click.exceptions import UsageError
import json
import logging
import HomeWorks.Lesson_4.logs.config_client_log
from HomeWorks.Lesson_4.errors import *
from HomeWorks.Lesson_4.common.functions import *
from HomeWorks.Lesson_4.decorators import log

client_logger = logging.getLogger('client')


@log
def create_exit_message(account_name):
    """" Функция создаёт словарь с сообщением о выходе."""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def message_from_server(sock, my_username):
    """" Функция - обработчик сообщений других пользователей, поступающих с сервера."""
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(
                    f'\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                client_logger.info(
                    f'Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            else:
                client_logger.error(
                    f'Получено некорректное сообщение с сервера: {message}')
        except IncorrectDataRecivedError:
            client_logger.error(
                f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
            client_logger.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, account_name='Guest'):
    """" Функция запрашивает кому отправить сообщение и само сообщение, и
        отправляет полученные данные на сервер."""
    to = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        client_logger.info(f'Отправлено сообщение для пользователя {to}')
    except ConnectionError:
        client_logger.critical('Потеряно соединение с сервером.')
        exit(1)


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


@log
def user_interactive(sock, username):
    """ Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения """
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            client_logger.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print(
                'Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


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


def print_help():
    """ Функция выводит справку по использованию."""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


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
@click.option('--name', '-n', default=None)
def start(port, addr, name):
    server_address = addr
    server_port = port
    client_name = name
    if server_port < 1024 or server_port > 65535:
        client_logger.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {server_port} сервера.'
            f'Допустимы адреса с 1024 до 65535.')
        exit(1)
    # Сообщаем о запуске
    print('Консольный месседжер. Клиентский модуль.')
    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not client_name:
        client_name = input('Введите имя пользователя: ')
    client_logger.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address} , порт: {server_port}, '
        f'имя пользователя: {client_name}')
    try:
        transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transfer_socket.connect((server_address, server_port))
        message_to_server = show_presence(client_name)
        send_message(transfer_socket, message_to_server)
        answer = proc_answer(get_message(transfer_socket))
        client_logger.info(f'Принят ответ от сервера {answer}')
        print(f'Установлено соединение с сервером.')
        print(f'Вы зарегистрированы как {client_name}')
    except json.JSONDecodeError:
        client_logger.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except ReqFieldMissingError as missing_error:
        client_logger.error(
            f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        client_logger.critical(
            f'Не удалось подключиться к серверу {server_address}:{server_port}, конечный компьютер отверг '
            f'запрос на подключение.')
        exit(1)
    else:
        # Если соединение с сервером установлено корректно, запускаем клиенский
        # процесс приёма сообщний
        receiver = threading.Thread(
            target=message_from_server, args=(
                transfer_socket, client_name))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(
            target=user_interactive, args=(
                transfer_socket, client_name))
        user_interface.daemon = True
        user_interface.start()
        client_logger.debug('Запущены процессы')

        # Watchdog основной цикл, если один из потоков завершён, то значит или потеряно соединение или пользователь
        # ввёл exit. Поскольку все события обработываются в потоках, достаточно
        # просто завершить цикл.
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    start()
