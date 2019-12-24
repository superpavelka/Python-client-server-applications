'''
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
результаты из байтовового в строковый тип на кириллице.
'''
import subprocess
import chardet

ARGS_YA = ['ping', 'yandex.ru']
ARGS_YOU = ['ping', 'youtube.com']

YA_PING = subprocess.Popen(ARGS_YA, stdout=subprocess.PIPE)
YOU_PING = subprocess.Popen(ARGS_YOU, stdout=subprocess.PIPE)

for line in YA_PING.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))

for line in YOU_PING.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
