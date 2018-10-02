import json, os

def filter_dict_list_by_key_value(list_of_dicts, key, value):
    filtered_list = [d for d in list_of_dicts if d[key] == value]
    return filtered_list

def get_single_dict_from_list(list_of_dicts, key, value):
    filtered_list = filter_dict_list_by_key_value(list_of_dicts, key, value)
    if len(filtered_list) > 1:
        raise AssertionError(f'More than 1 dict matched provided value, {value}, for key {key}.  Expecting 1 match.')
    elif len(filtered_list) == 0:
        raise AssertionError(f'No dict matched provided value, {value}, for key {key}.  Expecting 1 match.')
    return filtered_list[0]

def get_single_dict_from_json(filepath, key, value):
    with open(filepath, 'r') as f:
        json_list = json.load(f)
    return get_single_dict_from_list(json_list, key, value)

def get_full_path(filename, subfolder=None):
    cwd = os.getcwd()
    if subfolder:
        full_path = os.path.join(cwd, subfolder, filename)
    else:
        full_path = os.path.join(cwd, filename)
    return full_path