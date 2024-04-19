# Long Term Storage Script
## Installation

```sh
pip install -r requirements.txt
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
BUCKET_STORAGE_NAME

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```
## Usage

*For use in AWS lambda function.*

## Dockerfile

For building a docker image of the long term storage pipeline.

## Python script

### storage_load.py

Extracts recordings data from the RDS database which is at least 24 hours old and transfers it to an S3 bucket.

## Tests

### test_storage_load.py

Tests the script functions.

#### Usage:
```sh
pytest test_storage_load.py
```