# Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
# последовательность кодов (не используя методы encode и decode) и определить тип,
# содержимое и длину соответствующих переменных.

bytes_class = b'class'
bytes_function = b'function'
bytes_method = b'method'

print(type(bytes_class))
print(bytes_class)
print(len(bytes_class))

print(type(bytes_function))
print(bytes_function)
print(len(bytes_function))

print(type(bytes_method))
print(bytes_method)
print(len(bytes_method))
