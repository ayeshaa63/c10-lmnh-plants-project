source .env
sqlcmd -S $DB_HOST,$DB_PORT -U $DB_USER -P $DB_PASS -d $DB_NAME -i $1