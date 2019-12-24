'''
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''
from chardet.universaldetector import UniversalDetector

with open('test_file.txt', 'w') as f_n:
    f_n.write('сетевое программирование\n')
    f_n.write('сокет\n')
    f_n.write('декоратор')

try:
    with open('test_file.txt', encoding='utf-8') as f_n:
        for el_str in f_n:
            print(el_str, end='')
except UnicodeDecodeError:
    print('Ошибка декодирования т.к. кодировка файла отличается')

DETECTOR = UniversalDetector()
with open('test_file.txt', 'rb') as f_n:
    for line in f_n:
        DETECTOR.feed(line)
        if DETECTOR.done:
            break
    DETECTOR.close()
print('Кодировка файла по умолчанию: ' + DETECTOR.result['encoding'])

with open('test_file.txt', 'w', encoding='utf-8') as f_n:
    f_n.write('сетевое программирование\n')
    f_n.write('сокет\n')
    f_n.write('декоратор')

with open('test_file.txt', encoding='utf-8') as f_n:
    for el_str in f_n:
        print(el_str, end='')
