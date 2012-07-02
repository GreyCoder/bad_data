from bad_data_sql import get_department, get_customer, get_computer, get_mac
from bad_data import book_list, key_list

MainNDX = 0
for ndx in range(len(book_list)):
    MainNDX += 1
    department_id = get_department(book_list, ndx)
    customer_id = get_customer(book_list, ndx, department_id)
    computer_id = get_computer(book_list, ndx, customer_id,
                  key_list['date_keys'], key_list['computer_string_keys'])
    get_mac(book_list, ndx, computer_id, key_list['mac_address_keys'])
print 'Processed: ' + str(MainNDX)
