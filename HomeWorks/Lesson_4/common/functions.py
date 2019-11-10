from HomeWorks.Lesson_3.common.constants import*
import json


def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_SIZE)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise ValueError
    else:
        raise ValueError


def send_message(sock, message):
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
