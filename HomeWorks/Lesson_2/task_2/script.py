# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в
# файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с
# передачей в нее значений каждого параметра.


import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', encoding='utf-8') as f_n:
        data_to_json = json.load(f_n)
    dict_to_load = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": date
    }
    data_to_json["orders"].append(dict_to_load)

    with open('orders.json', 'w', encoding='utf-8') as f_n:
        json.dump(data_to_json, f_n, indent=4)



# Проверяем код

# Добавляем запись в json файл
#write_order_to_json('Paper', 5, 140, 'Smith', '24.09.2018')

# Добавляем еще запись в json файл
#write_order_to_json('Milk', 6, 260, 'Toren', '23.02.2019')


# Добавляем еще одну запись в json файл
write_order_to_json('Meat', 4, 750, 'Ivanov', '01.01.2010')
