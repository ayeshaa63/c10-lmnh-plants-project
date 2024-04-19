# ETL Script
## Installation

```sh
bash install.sh
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

To manually run the ETL Pipeline use the command:
```sh
python3 load.py
```

## Dockerfile

For building a docker image of the ETL pipeline.

## Python scripts

### extract.py

Extracts the data which is in JSON form, from an API endpoint and loads it a list of dictionaries. The list of dictionaries is returned for use in transform.py. The script uses multiprocessing to ensure speed because the script will be triggered every minute so it has a maximum of a minute to run.

### transform.py

Takes the key fields from the list of dictionaries passed in and creates a DataFrame. The data is then cleaned and normalised with errors being caught and handled appropriately. Any error that involves a sensor failure is put into a sensor failure list which is then passed to email_alert.py to give the recipients a warning. Email alert code is commented out so as not to run over the email limit on AWS. A DataFrame is returned.

### load.py

This script takes in a DataFrame of passed in plant information and uploads the data to their respective relations within the database. The database used is a Microsoft TSQL Database hosted on AWS RDS. The entire ETL Script is run from this file and so is the main script.

### insert_missing_metadata.py

Extracts and uploads metadata when `load.py` encounters a plant that doesn't exist in the database yet.

### email_alert.py

For sending email alerts when a problem is encountered in the data

### conftest.py

Useful functions for use in pytests.

## Tests

### test_extract.py

Tests the extract script functions.

#### Usage:
```sh
pytest test_extract.py
```

### test_transform.py

Tests the transform script functions.

#### Usage:
```sh
pytest test_transform.py
```

### test_load.py
Tests the load script functions.

#### Usage:
```sh
pytest test_load.py
```
