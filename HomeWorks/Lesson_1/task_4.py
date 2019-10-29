var_1_str = 'разработка'
var_2_str = 'администрирование'
var_3_str = 'protocol'
var_4_str = 'standard'

str_list = [var_1_str, var_2_str, var_3_str, var_4_str]

enc_bytes_list = []
for elem in str_list:
    elem_bytes = elem.encode('utf-8')
    enc_bytes_list.append(elem_bytes)

print(enc_bytes_list)

dec_str_list = []
for elem in enc_bytes_list:
    elem_str = elem.decode('utf-8')
    dec_str_list.append(elem_str)

print(dec_str_list)
