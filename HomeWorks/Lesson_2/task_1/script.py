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
    headers_list = []
    main_data = []

    pattern_1 = '^Изготовитель системы'
    pattern_2 = '^Название ОС'
    pattern_3 = '^Код продукта'
    pattern_4 = '^Тип системы'

    for i in range(1, n + 1):
        with open(f'info_{i}.txt') as f_n:
            for line in f_n:
                line = line.encode('utf-8').decode('utf-8')
                if re.match(pattern_1, line):
                    line = line.split(sep=':')
                    os_prod_list.append(line[1])
                    if line[0] in headers_list:
                        continue
                    else:
                        headers_list.append(line[0])
                elif re.match(pattern_2, line):
                    line = line.split(sep=':')
                    os_name_list.append(line[1])
                    if line[0] in headers_list:
                        continue
                    else:
                        headers_list.append(line[0])
                elif re.match(pattern_3, line):
                    line = line.split(sep=':')
                    os_code_list.append(line[1])
                    if line[0] in headers_list:
                        continue
                    else:
                        headers_list.append(line[0])
                elif re.match(pattern_4, line):
                    line = line.split(sep=':')
                    os_type_list.append(line[1])
                    if line[0] in headers_list:
                        continue
                    else:
                        headers_list.append(line[0])

    os_prod_list = [line.strip() for line in os_prod_list]
    os_name_list = [line.strip() for line in os_name_list]
    os_code_list = [line.strip() for line in os_code_list]
    os_type_list = [line.strip() for line in os_type_list]
    main_data.append(headers_list)
    j = 0
    while j < n:
        os_data_list = []
        for el in headers_list:
            if re.match(pattern_1, el):
                os_data_list.append(os_prod_list[j])
            elif re.match(pattern_2, el):
                os_data_list.append(os_name_list[j])
            elif re.match(pattern_3, el):
                os_data_list.append(os_code_list[j])
            elif re.match(pattern_4, el):
                os_data_list.append(os_type_list[j])
        main_data.append(os_data_list)
        j += 1
    return main_data


def write_to_csv(refer, n):
    with open(refer, 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in get_data(n):
            f_n_writer.writerow(row)

# Проверка работы


write_to_csv('os_data.csv', 3)
write_to_csv('os_data_1.csv', 3)