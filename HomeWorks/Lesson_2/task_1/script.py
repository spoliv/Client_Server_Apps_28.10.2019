# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных
# из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
# Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
# данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
# соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data —
# и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data
# (также для каждого файла);
# Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
# данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
# Проверить работу программы через вызов функции write_to_csv().


import re
import csv

# n - количество обрабатываемых файлов


def get_data(n):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = []

    headers_list = [
        'Изготовитель системы',
        'Название ОС',
        'Код продукта',
        'Тип системы']
    main_data.append(headers_list)
    for i in range(1, n + 1):
        os_data_list = []
        with open(f'info_{i}.txt') as f_n:
            for line in f_n:
                line = line.encode('utf-8').decode('utf-8')
                for j in range(4):
                    if re.match(headers_list[j], line):
                        line = line.split(sep=':')
                        line_1 = line[1].strip()
                        os_data_list.insert(j, line_1)
                        if j == 0:
                            os_prod_list.append(line_1)
                            break
                        elif j == 1:
                            os_name_list.append(line_1)
                            break
                        elif j == 2:
                            os_code_list.append(line_1)
                            break
                        else:
                            os_type_list.append(line_1)
        main_data.append(os_data_list)
    return main_data


def write_to_csv(refer, n):
    with open(refer, 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in get_data(n):
            f_n_writer.writerow(row)

# Проверка работы


write_to_csv('os_data.csv', 3)
write_to_csv('os_data_1.csv', 3)
