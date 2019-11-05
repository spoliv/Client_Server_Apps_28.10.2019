# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в
# файле YAML-формата. Для этого:
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое
# число, третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
# отсутствующим в кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить
# стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: \
#     allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают
# ли они с исходными.

import yaml


items = ['bread', 'milk', 'meat']
a = 5
dic_in = {
    'price_in_dol': '5$',
    'price_in_euro': '7€',
    'price_in_pound': '2£'
}

data_to_yaml = {'products': items,
                'num': a,
                'prices': dic_in
                }
with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(data_to_yaml, f_n, default_flow_style=False, allow_unicode=True)

with open('file.yaml', encoding='utf-8') as f_n:
    print(f_n.read())
