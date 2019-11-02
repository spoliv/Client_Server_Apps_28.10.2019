# Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
# «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в
# формате Unicode и вывести его содержимое.

import locale

a = ['сетевое программирование', 'сокет', 'декоратор']
with open('test_file.txt', 'w', encoding='utf-8') as f_n:
    # f_n.write(
    #     'сетевое программирование' +
    #     '\n' +
    #     'сокет' +
    #     '\n' +
    #     'декоратор' +
    #     '\n')
    a = map(lambda x: x + '\n', a)
    f_n.writelines(a)


print(locale.getpreferredencoding())

with open('test_file.txt', encoding='utf-8') as f_n:
    for line in f_n:
        line = line.encode('utf-8').decode('utf-8')
        print(line, end='')
