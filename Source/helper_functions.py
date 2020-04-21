def print_dictionary_in_rows(new_dict):
    '''Nice output of key:vals in rows'''
    for key,val in new_dict.items():
        print('{}: {}'.format(key, val))

def remove_utf_charactars_and_strip(text):
    '''removes strange characters and also things such --> OPTIFAST® VLCD™ '''
    return text.encode('ascii',errors='ignore').decode('utf-8').lstrip().rstrip()

def remove_list_duplicates(dupl_list):
    return list(set(dupl_list))


def get_tables_by_th_name(dict_table_names_wanted, children_tbody):
    '''Pass a dictionary with keys being the names (these names are in the table headers) of tables you want and
    pass a list object full of html tables, it will return a dictionary of those html tables corresponding
    to the names'''
    
    for table in children_tbody:
        children_headers = table.findChildren("th" , recursive=True)
        children_headers = remove_list_duplicates(children_headers)
        for child in children_headers:
            name = child.text
            if name in dict_table_names_wanted:
                dict_table_names_wanted[name] = table

    return dict_table_names_wanted