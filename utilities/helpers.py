import json, os
from functools import wraps


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

def get_connection_details(connection_name):
    connections_path = get_full_path(filename='connections.json', subfolder='settings')
    connection_dict = get_single_dict_from_json(connections_path, 'connection_name', connection_name)
    return connection_dict

def attempt_three_executions(logger):
    def attempt_three_executions_decarator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < 3:
                try:
                    function(*args, **kwargs)
                    break
                except:
                    attempts += 1
                    logger.warning(f"Failed to execute {function.__name__} on attempt # {attempts}.")
            else:
                logger.error(f"Terminal failure to execute {function.__name__}.")
                raise Exception(f"Terminal failure to execute {function.__name__}.")
        return wrapper
    return attempt_three_executions_decarator