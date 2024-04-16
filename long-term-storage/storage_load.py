"""
This script is to extract and remove the out-of-date data from the database 
 it into long-term storage in an S3 bucket.
"""
from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv
import pandas as pd
from pymssql import connect, Connection


def connect_to_db(config) -> Connection:
    """Connects to the short-term plants database."""
    return connect(
        server=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        port=config["DB_PORT"],
        as_dict=True
    )


def get_recent_entries(conn: Connection) -> None:
    """Goes into database, and pulls all entries in the plant table which have
    a recording older than 24 hours. Returns a CSV file."""
    with conn.cursor() as cur:
        cur.execute("""SELECT p.* FROM s_alpha.plant AS p
                    JOIN s_alpha.recordings AS r
                    ON (r.plant_id = p.plant_id)
                    WHERE DATEDIFF(hour, CURRENT_TIMESTAMP, r.timestamp) > 24;""")
        print(cur.fetchall())


def load_csv_file() -> None:
    """Given our recent entries, we now connect to an S3 bucket and load."""
    pass


def storage_load():
    """To be solely run when executing this Python script."""
    pass


if __name__ == "__main__":

    load_dotenv()

    conn = connect_to_db(ENV)

    print(get_recent_entries(conn))
