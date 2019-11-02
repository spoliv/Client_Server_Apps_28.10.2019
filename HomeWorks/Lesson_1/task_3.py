# Определить, какие из слов «attribute», «класс», «функция», «type»
# невозможно записать в байтовом типе.

var_1 = 'attribute'
var_2 = 'класс'
var_3 = 'функция'
var_4 = 'type'

var_list = [var_1, var_2, var_3, var_4]

for elem in var_list:
    try:
        print(bytes(elem, 'ascii'))
    except UnicodeEncodeError:
        print(f'Слово "{elem}" невозможно записать в виде байтовой строки')
