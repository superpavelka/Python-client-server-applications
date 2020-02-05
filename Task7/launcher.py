import subprocess

PROC = []

while True:
    ACTION = input('Выберите действие: s - запустить сервер и клиенты, q - выход, x - закрыть все окна: ')

    if ACTION == 's':
        PROC.append(subprocess.Popen('python server.py',
                                     creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(2):
            PROC.append(subprocess.Popen('python client.py -m send',
                                         creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(5):
            PROC.append(subprocess.Popen('python client.py -m listen',
                                         creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'q':
        break

    elif ACTION == 'x':
        while PROC:
            VICTIM = PROC.pop()
            VICTIM.kill()
