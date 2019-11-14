import json
from HomeWorks.Lesson_4.common.constants import*
from HomeWorks.Lesson_4.errors import IncorrectDataRecivedError, NonDictInputError


def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_SIZE)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise IncorrectDataRecivedError
    else:
        raise IncorrectDataRecivedError


def send_message(sock, message):
    if not isinstance(message, dict):
        raise NonDictInputError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
