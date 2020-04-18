def print_dictionary_in_rows(new_dict):
    '''Nice output of key:vals in rows'''
    for key,val in new_dict.items():
        print('{}: {}'.format(key, val))

def remove_utf_charactars_and_strip(text):
    '''removes strange characters and also things such --> OPTIFAST® VLCD™ '''
    return text.encode('ascii',errors='ignore').decode('utf-8').lstrip().rstrip()

def remove_list_duplicates(dupl_list):
    return list(set(dupl_list))