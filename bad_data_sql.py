from sqlalchemy import Table, Column, ForeignKey, MetaData
from sqlalchemy.dialects.mysql import VARCHAR, BOOLEAN, TEXT, INTEGER, DATE
from datetime import datetime
from config import engine

metadata = MetaData()

connection = engine.connect()

department = Table(
    'Department',
    metadata,
    Column('id', INTEGER, primary_key=True),
    Column('name', VARCHAR(127), nullable=False),
    )

customer = Table(
    'Customer',
    metadata,
    Column('id', INTEGER, primary_key=True),
    Column('first_name', VARCHAR(127), nullable=False),
    Column('last_name', VARCHAR(127), nullable=False),
    Column('department_id', INTEGER, ForeignKey('department.id'), nullable=True)
    )

computer = Table(
    'Computer',
    metadata,
    Column('id', INTEGER, primary_key=True),
    Column('customer_id', INTEGER, ForeignKey('customer.id'), nullable=False),
    Column('po_number', VARCHAR(127), nullable=True),
    Column('hw_type', TEXT, nullable=True),
    Column('customization', TEXT, nullable=True),
    Column('notes', TEXT, nullable=True),
    Column('configured_by', TEXT, nullable=True),
    Column('date_ready', DATE, nullable=True),
    Column('date_computer_ordered', DATE, nullable=True),
    Column('date_deployed', DATE, nullable=True),
    Column('date_posted_to_rh_ss', DATE, nullable=True),
    Column('image', VARCHAR(127), nullable=True),
    Column('is_mac', BOOLEAN, nullable=True),
    Column('heaf', VARCHAR(10), nullable=True),
    Column('asset_tag', VARCHAR(127), nullable=True),
    Column('serial_computer', VARCHAR(127), nullable=True),
    Column('change_computer', VARCHAR(127), nullable=True)
    )

mac_address = Table(
    'MAC_Address',
    metadata,
    Column('id', INTEGER, primary_key=True),
    Column('address', VARCHAR(32), nullable=False),
    Column('name', VARCHAR(32), nullable=False),
    Column('computer_id', INTEGER, ForeignKey('computer.id'), nullable=False)
    )


def get_department(book_list, ndx):
    department_id = None
    if book_list[ndx]['department'] is not None:

        exists_department_select_query = department.select().\
                where(department.c.name == str(book_list[ndx]['department']))

        select_results = connection.execute(exists_department_select_query).\
                            fetchone()
        if select_results is None:
            insert_query = department.insert().\
                values(name=str(book_list[ndx]['department']))
            result = connection.execute(insert_query)
            department_id = int(result.last_inserted_ids()[0])
        else:
            if 'id' in select_results:
                department_id = select_results['id']
            else:
                department_id = None
    else:
        department_id = None
    return department_id


def get_customer(book_list, ndx, department_id):
    if type(book_list[ndx]['first_name']) is not None and\
    type(book_list[ndx]['last_name']) is not None:

        exists_customer_select_query = customer.select().\
            where(customer.c.first_name == str(book_list[ndx]['first_name'])).\
            where(customer.c.last_name == str(book_list[ndx]['last_name']))

    single_customer = {'first_name': str(book_list[ndx]['first_name']),
                        'last_name': str(book_list[ndx]['last_name'])}
    if department_id is not None:
        single_customer['department_id'] = department_id
        select_results = connection.execute(exists_customer_select_query).\
                        fetchone()
    if select_results is None:
        insert_customer_query = customer.insert().values(single_customer)
        result = connection.execute(insert_customer_query)
        customer_id = int(result.last_inserted_ids()[0])
    else:
        if 'id' in select_results:
            customer_id = int(select_results['id'])
        else:
            print 'id not in customer'
            customer_id = None
    return customer_id


def get_computer(book_list, ndx, customer_id, date_keys, computer_string_keys):
    computer_dict = {}
    computer_id = None
    computer_dict['customer_id'] = customer_id
    for date_field in date_keys:
        if date_field in book_list[ndx] and book_list[ndx][date_field] != None\
        and type(book_list[ndx][date_field]) is datetime:
            computer_dict[date_field] = book_list[ndx][date_field]

    if type(book_list[ndx]['mac']) is bool:
        computer_dict['is_mac'] = book_list[ndx]['mac']
    if book_list[ndx]['mac'] is None:
        computer_dict['is_mac'] = False

    for computer_string in computer_string_keys:
        if book_list[ndx][computer_string] is not None:
            if type(book_list[ndx][computer_string]) is not unicode and\
            type(book_list[ndx][computer_string]) is not str:
                computer_dict[computer_string] = str(
                                                book_list[ndx][computer_string]
                                                )
            else:
                computer_dict[computer_string] = book_list[ndx][computer_string]

    computer_insert_query = computer.insert().values(computer_dict)
    result = connection.execute(computer_insert_query)
    computer_id = int(result.last_inserted_ids()[0])
    return computer_id


def get_mac(book_list, ndx, computer_id, mac_address_keys):
    mac_dict = {}
    if computer_id is not None:
        mac_dict = {}
        mac_dict['computer_id'] = computer_id
        for mac in mac_address_keys:
            if book_list[ndx][mac] is not None:
                mac_dict['name'] = mac
                mac_dict['address'] = str(book_list[ndx][mac])
                mac_insert_query = mac_address.insert().values(mac_dict)
                connection.execute(mac_insert_query)
