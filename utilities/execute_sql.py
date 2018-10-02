import sqlalchemy as sa 


def execute_sql_string(connection_manager, raw_sql_string):
    sql_list = raw_sql_string.split(';')
    results = []
    cleaned_sql_list = [sql for sql in sql_list if sql]
    for sql_statement in cleaned_sql_list:
        connection_manager.connect()
        result = connection_manager.conn.execute(sql_statement)
        headers = result.keys()
        result_list = [tuple(headers)] + result.fetchall()
        results.append(result_list)
        connection_manager.close()
    return results


def execute_sql_from_file(connection_manager, filepath):
    with open(filepath, 'r') as sql_file:
        raw_sql_string = sql_file.read()
    result = execute_sql_string(connection_manager, raw_sql_string)
    return result


def execute_stored_procedure(connection_manager, sp_name, sp_arguments_list=None):
    sp_arguments = ', '.join(sp_arguments_list) if sp_arguments_list else ''
    if connection_manager.db_type == 'mysql':
        sql_string = f'call {sp_name}({sp_arguments})'
    else:
        raise AssertionError(f'Stored procedures not supported for database type {connection_manager.db_type}')
    result = execute_sql_string(connection_manager, sql_string)
    return result


def convert_results_to_2d_list(results):
    pass
