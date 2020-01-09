'''
Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое
число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''
import yaml

ITEMS = ['computer', 'printer', 'keyboard']
QUANTITY = 3
PRICE = {'computer': '200€ - 1000€', 'printer': '100€ - 300€', 'keyboard': '5€ - 50 €'}
DATA_TO_YAML = {'items': ITEMS, 'quantity': QUANTITY, 'price': PRICE}

with open('data_write.yaml', 'w') as f_n:
    yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False, allow_unicode=True)

with open('data_write.yaml') as f_n:
    print(f_n.read())
