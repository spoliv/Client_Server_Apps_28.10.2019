import subprocess

process = []

while True:
    action = input(
        'Выберите действие: q - выход , s - запустить сервер и клиенты, x - закрыть все окна:')

    if action == 'q':
        break
    elif action == 's':
        process.append(
            subprocess.Popen(
                'python server.py',
                creationflags=subprocess.CREATE_NEW_CONSOLE))
        process.append(
            subprocess.Popen(
                'python client.py -n Olga',
                creationflags=subprocess.CREATE_NEW_CONSOLE))
        process.append(
            subprocess.Popen(
                'python client.py',
                creationflags=subprocess.CREATE_NEW_CONSOLE))
        process.append(
            subprocess.Popen(
                'python client.py -n Gena',
                creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif action == 'x':
        while process:
            victim = process.pop()
            victim.kill()
