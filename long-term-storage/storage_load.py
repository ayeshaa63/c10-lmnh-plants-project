"""
This script is to extract and remove the out-of-date data from the database, and 
transport it into long-term storage in an S3 bucket, where it is stored in CSV files.
"""
from datetime import datetime
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


def get_recent_recordings(conn: Connection, current_timestamp: datetime,
                          config) -> pd.DataFrame:
    """Goes into database, and pulls all entries in the recording table with a timestamp
    older than 24 hours."""
    with conn.cursor() as cur:
        cur.execute(f"""SELECT r.*
                    FROM {config["SCHEMA"]}.recording AS r
                    WHERE DATEDIFF(hour, %s, r.timestamp) > 24;""",
                    (current_timestamp,))

        result = cur.fetchall()

    conn.commit()
    cur.close()

    return pd.DataFrame(result)


def del_recent_recordings(conn: Connection, current_timestamp: datetime, config) -> None:
    """Goes into database, and deletes all entries in the recording table with a timestamp
    older than 24 hours."""
    with conn.cursor() as cur:
        cur.execute(f"""DELETE r.*
                    FROM {config["SCHEMA"]}.recording AS r
                    WHERE DATEDIFF(hour, %s, r.timestamp) > 24;""",
                    (current_timestamp,))

    conn.commit()
    cur.close()


def create_current_datetime_filename(current_timestamp: datetime) -> str:
    """Given the current timestamp, a CSV filename is created."""
    current_yr = current_timestamp.year
    current_mth = current_timestamp.month
    current_day = current_timestamp.day
    current_hr = current_timestamp.hour
    current_min = current_timestamp.minute

    return f"{current_yr}/{current_mth}/{current_day}/{current_hr}:{current_min}"


def convert_data_csv_file(data: pd.DataFrame, csv_filename: str) -> None:
    """Given a pd.DataFrame object, we convert it into CSV format."""
    data.to_csv(csv_filename, index=False)


def load_csv_file(s3_client: client, csv_filename: str, config) -> None:
    """Given a CSV file, we now connect to an S3 bucket and load."""
    s3_client.upload_file(Bucket=config["BUCKET_STORAGE_NAME"],
                          Filename=csv_filename,
                          Key=csv_filename)


if __name__ == "__main__":

    current_timestamp = datetime.now()

    load_dotenv()

    conn = connect_to_db(ENV)

    old_recordings = get_recent_recordings(conn, current_timestamp, ENV)

    del_recent_recordings(conn, current_timestamp, ENV)

    csv = f"{create_current_datetime_filename(current_timestamp)}.csv"

    convert_data_csv_file(old_recordings, csv)

    s3 = client("s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    load_csv_file(s3, csv, ENV)
