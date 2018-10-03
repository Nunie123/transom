import argparse, os, sys, subprocess

from utilities.write_logs import Logger
from utilities.helpers import get_connection_details

logger = Logger(__file__)


def copy_table(source_connection,
                destination_connection,
                table_name,
                source_db='',
                destination_db='',
                source_schema='',
                destination_schema='',
                timeout=1800):

    source_connection_details = get_connection_details(source_connection)
    destination_connection_details = get_connection_details(destination_connection)

    env_vars = [
        ('TIMEOUT', str(timeout)),
        ('SOURCE_HOST', source_connection_details['host']),
        ('SOURCE_USER', source_connection_details['username']),
        ('SOURCE_PASSWORD', source_connection_details['password']),
        ('SOURCE_SCHEMA', source_schema),
        ('SOURCE_DB', source_db),
        ('TABLE_NAME', table_name),
        ('DESTINATION_HOST', destination_connection_details['host']),
        ('DESTINATION_USER', destination_connection_details['user']),
        ('DESTINATION_PASSWORD', destination_connection_details['password']),
        ('DESTINATION_SCHEMA', destination_schema),
        ('DESTINATION_DB', destination_db),
        ('SOURCE_DB_TYPE', source_connection_details['db_type']),
        ('DESTINATION_DB_TYPE', destination_connection_details['db_type'])
    ]

    for key, value in env_vars:
        os.environ[key] = value

    try:
        logger.info("Performing table copy for {}.{}.".format(source_schema, table_name))

        retcode = subprocess.call("./copy_table.sh")

        if retcode == 0:
            logger.info("Copied table {}.{} successfully.".format(destination_schema, table_name))
        else:
            logger.warning("Failed to copy table {}.{}. Return code {}".format(source_schema, table_name, retcode))
            raise AssertionError()
    except OSError as e:
        print("-- OSError - execution failed:", e, file=sys.stderr)
        raise e

