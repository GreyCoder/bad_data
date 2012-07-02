import re
from datetime import datetime
from xlrd import open_workbook, xldate_as_tuple

book = open_workbook('combined.xls')
sheet = book.sheet_by_index(0)
key_list = {}
key_list['date_keys'] = ['date_posted_to_rh_ss', 'date_ready', 'date_deployed',
                        'date_computer_ordered']

key_list['computer_string_keys'] = ['configured_by', 'image', 'customization',
                                'serial_computer', 'heaf', 'change_computer',
                                'asset_tag', 'notes', 'po_number', 'hw_type']

key_list['possible_computer_id'] = ['serial_computer', 'asset_tag',
                                    'po_number']

key_list['mac_address_keys'] = ['machine_address1', 'machine_address2',
                                'machine_address3']


def generate_dictionary(sheet):
    '''This function takes 1 argument
        `sheet` is the excel spreadsheet in xlrd format
        This function will parse the xlrd dictionary and return
        a python list of dictionaries with the row numbers as an
        index and the column names as keys
    '''
    book_list = []
    for ndx in range(sheet.nrows - 1):
        book_list.append({})
        for ndx2 in range(sheet.ncols):
            book_list[ndx][str(sheet.cell(0, ndx2).value)] =\
                        sheet.row_values(ndx + 1)[ndx2]
    return book_list


def clean_dates(book_list, key_list):
    for entry in book_list:
        for date_key in key_list['date_keys']:
            if type(entry[date_key]) is str and str(len(entry[date_key])) < 1:
                entry[date_key] = None
            if type(entry[date_key]) is float:
                date_value = xldate_as_tuple(entry[date_key],
                book.datemode)
                entry[date_key] = datetime(*date_value)
            elif len(entry[date_key]) == 0:
                entry[date_key] = None
    return book_list


def clean_macs(book_list, key_list):
    mac_pattern = re.compile(r'[\`\s\']*([A-Fa-f0-9]{2})[\s\-\:]*([A-Fa-f0-9]{2})[\s\-\:]*([A-Fa-f0-9]{2})[\s\-\:]*([A-Fa-f0-9]{2})[\s\-\:]*([A-Fa-f0-9]{2})[\s\-\:]*([A-Fa-f0-9]{2})')
    for entry in book_list:
        for mac in key_list['mac_address_keys']:
            if type(entry[mac]) is float:
                entry[mac] = str(int(
                                    entry[mac]))
                while len(entry[mac]) < 12:
                    entry[mac] = '0' + entry[mac]
            mac1 = mac_pattern.match(entry[mac])
            if mac1:
                entry[mac] = mac1.expand(r'\1\2\3\4\5\6')
            if type(entry[mac]) is str or \
                type(entry[mac]) is unicode:
                if len(entry[mac]) < 1:
                    entry[mac] = None
                elif 'n/a' in entry[mac]:
                    entry[mac] = None
                elif 'none' in entry[mac]:
                    entry[mac] = None
    return book_list


def clean_change_computer(book_list):
    for entry in book_list:
        if entry['change_computer'] != '':
            if entry['change_computer'] == 'm>w':
                entry['change_computer'] = 'Mac to Windows'
            if entry['change_computer'] == 'w>m':
                entry['change_computer'] = 'Windows to Mac'
    return book_list


def clean_customization(book_list):
    for entry in book_list:
        if entry['customization'] != '':
            if len(str(entry['customization'].\
                    encode('latin-1', 'ignore'))) <= 2:
                entry['customization'] = None
        else:
            entry['customization'] = None
    return book_list


def clean_ismac(book_list):
    for entry in book_list:
        if 'm' in entry['mac'].strip():
            entry['mac'] = True
        elif entry['mac'] == '' or entry['mac'] == None:
            entry['mac'] = False
    return book_list


def clean_department(book_list):
    for entry in book_list:
        if entry['department'] is not None:
            entry['department'] = str(entry['department'])
    return book_list


def clean_string_keys(book_list, key_list):
    for entry in book_list:
        for string_key in key_list['computer_string_keys']:
            if type(entry[string_key]) is float:
                entry[string_key] = int(entry[string_key])
            if entry[string_key] is not None:
                if type(entry[string_key]) is str or\
                    type(entry[string_key]) is unicode:
                    entry[string_key] = entry[string_key].\
                                            encode('latin-1', 'ignore')
                    if len(entry[string_key]) < 1:
                        entry[string_key] = None
                else:
                    entry[string_key] = str(entry[string_key]).\
                                            encode('latin-1', 'ignore')
                    if len(entry[string_key]) < 1:
                        entry[string_key] = None
    return book_list


book_list = generate_dictionary(sheet)
book_list = clean_dates(book_list, key_list)
book_list = clean_macs(book_list, key_list)
book_list = clean_change_computer(book_list)
book_list = clean_customization(book_list)
book_list = clean_ismac(book_list)
book_list = clean_department(book_list)
book_list = clean_string_keys(book_list, key_list)
