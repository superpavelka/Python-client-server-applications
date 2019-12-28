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


def get_data(p_man, p_os_name, p_code, p_os_type, f_names, m_data):
    '''returns data by patterns from file list'''
    man_lst = []
    os_name_lst = []
    code_lst = []
    os_type_lst = []

    for name in f_names:
        with open(name, 'rb') as f_n:
            data = f_n.read()
            enc = detect(data)['encoding']
        with open(name, encoding=enc) as f_n:
            data = f_n.read()
            print(data)
        man_lst.append(re.findall(p_man, data))
        os_name_lst.append(re.findall(p_os_name, data))
        code_lst.append(re.findall(p_code, data))
        os_type_lst.append(re.findall(p_os_type, data))
    for i in range(len(f_names)):
        spam_lst = []
        spam_lst.append(man_lst[i][0])
        spam_lst.append(os_name_lst[i][0])
        spam_lst.append(code_lst[i][0])
        spam_lst.append(os_type_lst[i][0])
        m_data.append(spam_lst)
    return m_data


def write_to_csv(f_n, data):
    '''writes data to f_n in csv'''
    csv_writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerows(data)


if __name__ == "__main__":
    PAT_MAN = re.compile('Изготовитель системы: +(\w+)')
    PAT_OS_NAME = re.compile('Название ОС: +(\w+ \w+ \d\.?\d? \w+)')
    PAT_CODE = re.compile('Код продукта: +(\w+-\w+-\w+-\w+)')
    PAT_OS_TYPE = re.compile('Тип системы: +(\w+-\w+ \w+)')

    FILE_NAMES = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    MAIN_DATA = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    with open('main_data.csv', 'w') as f:
        write_to_csv(f, get_data(PAT_MAN, PAT_OS_NAME, PAT_CODE, PAT_OS_TYPE, FILE_NAMES, MAIN_DATA))
