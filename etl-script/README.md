# ETL Script
## Installation

```sh
bash install.sh
```

## Usage

```sh
python3 load.py
```

## Dockerfile

For building a docker image of the ETL pipeline.

## Python scripts

### extract.py

Extracts the data which is in JSON form, from an API endpoint and loads it into a pandas dataframe. The dataframe is passed to extract.py

### transform.py

Cleans and normalises the data within the passed in dataframe. The dataframe is passed to transform.py.

### load.py

Uploads a passed in dataframe to the Microsoft SQL Server database.

### insert_missing_metadata.py

Extracts and uploads metadata when `load.py` encounters a plant that doesn't exist in the database yet.

### email_alert.py

For sending email alerts when a problem is encountered in the data

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