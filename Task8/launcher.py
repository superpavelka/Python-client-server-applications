import subprocess

PROC = []

while True:
    ACTION = input('Выберите действие: s - запустить сервер и клиенты, q - выход, x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROC.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROC.append(subprocess.Popen('python client.py -n Vasya',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROC.append(subprocess.Popen('python client.py -n Petya',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROC.append(subprocess.Popen('python client.py -n Anonymous',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROC:
            VICTIM = PROC.pop()
            VICTIM.kill()
