'''
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью
регулярных выражений извлечь значения параметров «Изготовитель системы», «Название ОС»,
«Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
os_type_list. В этой же функции создать главный список для хранения данных отчета —
например, main_data — и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции
реализовать получение данных через вызов функции get_data(), а также сохранение подготовленных
данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
'''

import csv
import re
from chardet import detect

PAT_MAN = re.compile('Изготовитель системы: +(\w+)')
PAT_OS_NAME = re.compile('Название ОС: +(\w+ \w+ \d\.?\d? \w+)')
PAT_CODE = re.compile('Код продукта: +(\w+-\w+-\w+-\w+)')
PAT_OS_TYPE = re.compile('Тип системы: +(\w+-\w+ \w+)')

FILE_NAMES = ['info_1.txt','info_2.txt','info_3.txt']
MAIN_DATA = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

MAN_LST = []
OS_NAME_LST = []
CODE_LST = []
OS_TYPE = []

for name in FILE_NAMES:
    with open(name, 'rb') as f_n:
        data = f_n.read()
        enc = detect(data)['encoding']
    with open(name, encoding=enc) as f_n:
        data = f_n.read()
        print(data)
    MAN_LST.append(re.findall(PAT_MAN, data))
    OS_NAME_LST.append(re.findall(PAT_OS_NAME, data))
    CODE_LST.append(re.findall(PAT_CODE, data))
    OS_TYPE.append(re.findall(PAT_OS_TYPE, data))
    print(MAN_LST)
    print(OS_NAME_LST)
    print(CODE_LST)
    print(OS_TYPE)