# c10-lmnh-plants-project

## ETL Scripts

### extract.py

Extracts the data which is in JSON form, from an API endpoint and loads it into a pandas dataframe. The dataframe is passed to extract.py

### transform.py

Cleans and normalises the data within the passed in dataframe. The dataframe is passed to transform.py.

### load.py

Uploads a passed in dataframe to the Microsoft SQL Server database.


## Long Term Storage Loading

## storage_load.py

Moves any row that is more than 24 hours old from the Microsoft SQL Server database short term storage to an S3 Bucket for long term storage.


## Unit Testing

*/test-*.py
