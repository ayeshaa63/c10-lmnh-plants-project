# c10-lmnh-plants-project


## Requirements


To install requirements, if you want to run the scripts manually, run this command line in the root of the directory within a virtual environment:
```sh
pip3 install -r requirements.txt
```
The following are all the requirements for all the scripts to run within the project:
```sh
pandas
python-dotenv
pymssql
pytest
pylint
pytest-mock
requests-mock
aiohttp
boto3
```

## Directories

### etl-script

{INFO ABOUT ETL SCRIPTS HERE}


### long-term-storage

{INFO}

### schema

{INFO}

### terraform

{INFO}

## Useful scripts

### activate_venv.sh

Easily build and enter a venv with
```sh
bash activate_venv.sh
```

### connect_to_db.sh

The following env variables must be accessible to the script:
```sh
DB_HOST
DB_NAME
DB_USER
DB_PASS
DB_PORT
```

Then easily connect to the database with
```sh
bash connect_to_db.sh
```