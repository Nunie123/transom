#!/bin/bash

set -euo pipefail

if [$SOURCE_DB_TYPE == 'mysql'] && [$DESTINATION_DB_TYPE == 'mysql']
then
    copy_mysql_table () {
        timeout -s 9 $TIMEOUT \
        mysqldump -h $SOURCE_HOST -u $SOURCE_USER --password="$SOURCE_PASSWORD" --lock-tables=FALSE $SOURCE_SCHEMA $TABLE_NAME |
        mysql -h $DESTINATION_HOST -u $DESTINATION_USER  --password="$DESTINATION_PASSWORD" $DESTINATION_SCHEMA
    }
fi