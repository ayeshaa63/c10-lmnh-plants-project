# Schema set up
## Installation

```sh
`brew install sqlcmd`
pip install -r requirements
```
### Environment variables

The following env variables must be accessible to the script:
```sh
DB_HOST
DB_NAME
DB_USER
DB_PASS
DB_PORT
SCHEMA_NAME
```


## Usage

To reset the database to empty tables, run:
```sh
bash reset.sh schema.sql
```
To insert some basic metadata into the newly built database, run:
```sh
python3 insert_metadata.py
```

## Python script

### insert_metadata.py

Extracts recordings data from the RDS database which is at least 24 hours old and transfers it to an S3 bucket.

## T-SQL script

### schema.sql

Drops old tables, and any data inside them, from the database. Then build empty tables, setting relevant constraints for keys and datatypes.
