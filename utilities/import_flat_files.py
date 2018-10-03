from utilities.helpers import get_connection_details
from utilities.execute_sql import execute_sql_string

def import_csv_to_mysql(connection_manager, file_location, destination_schema, destination_table, truncate_table=False, first_row_headers=True):
    standardize_csv_line_endings(file_location)
    raw_sql = f'TRUNCATE TABLE {destination_schema}.{destination_table};' if truncate_table else ''
    raw_sql = f'LOAD DATA LOCAL INFILE "{file_location}"' \
            + f'INTO TABLE {destination_schema}.{destination_table}' \
            + f'FIELDS TERMINATED BY ","' \
            + f'LINES TERMINATED BY "\n"'
    raw_sql = raw_sql + 'IGNORE 1 LINES;' if first_row_headers else ''
    execute_sql_string(connection_manager, raw_sql)

def standardize_csv_line_endings(file_location):
    fileContents = open(file_location,"r").read()
    f = open(file_location,"w", newline="\n")
    f.write(fileContents)
    f.close()