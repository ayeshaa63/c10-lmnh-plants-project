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


def find_row_index_most_sim(df: pd.DataFrame) -> int:
    """Given a dataframe with temp and soil_moisture columns, it finds the row index 
    of the row which is the closest match to the means of temp and soil_moisture."""
    df_temp_mean = df["temp"].mean()
    df_soil_mean = df["soil_moisture"].mean()

    # We rank temperature and soil moisture based on how close they are to their
    # respective means.
    df_rank = df
    df_rank["temp"] = df_rank["temp"].sub(
        df_temp_mean).abs().apply(pd.Series.rank).astype(int)
    df_rank["soil_moisture"] = df_rank["soil_moisture"].sub(
        df_soil_mean).abs().apply(pd.Series.rank).astype(int)

    # Finally, we sum up the ranks for each column, and the row with
    # the least rank sum is our most similar row!
    df_rank["rank_sum"] = df_rank[[
        "temp", "soil_moisture"]].sum(axis=1)
    i = df_rank["rank_sum"].min().index

    return i


def remove_sim_soil_moist_temp_values(df: pd.DataFrame) -> pd.DataFrame:
    """Looks into the input dataframe, and for each plant, drops all soil moisture and
    temperature values that are non-outliers (ie. within 2 sample SDs)."""

    plant_id_list = df["plant_id"].unique().tolist()

    for plant_id in plant_id_list:
        df_id = df[df["plant_id"] == plant_id][["temp", "soil_moisture"]]
        # We firstly find what recording in the series has the closest value to the
        # mean of the temp and soil moisture, and then find the index of the row most
        # closely resembling the means of temp and soil moisture.
        df_id_temp_mean = df_id["temp"].mean()
        df_id_soil_mean = df_id["soil_moisture"].mean()
        most_sim_row_index = find_row_index_most_sim(df_id)
        df_id_sim_row = df_id.iloc[most_sim_row_index]

        # We remove all non-outlier values in temp and soil moisture.
        temp_lower = df_id_temp_mean - 2 * df_id["temp"].std(ddof=0)
        temp_upper = df_id_temp_mean + 2 * df_id["temp"].std(ddof=0)
        df_id = df_id.drop(df_id[df_id["temp"] > temp_lower &
                                 df_id["temp"] < temp_upper])

        soil_lower = df_id_soil_mean - 2 * df_id["soil_moisture"].std(ddof=0)
        soil_upper = df_id_soil_mean + 2 * df_id["soil_moisture"].std(ddof=0)
        df_id = df_id.drop(df_id[df_id["soil_moisture"] > soil_lower
                           & df_id["soil_moisture"] < soil_upper])

        # We finally append the most similar row back into the resultant dataframe.
        df_id = df_id.append(df_id_sim_row, ignore_index=True)

        df[df["plant_id"] == plant_id] = df_id

    return df


def create_current_datetime_filename(current_timestamp: datetime) -> str:
    """Given the current timestamp, a CSV filename is created."""
    current_yr = current_timestamp.year()
    current_mth = current_timestamp.month()
    current_day = current_timestamp.day()
    current_hr = current_timestamp.hour()
    current_min = current_timestamp.minute()

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

    recordings_df = remove_sim_soil_moist_temp_values(old_recordings)

    csv = f"{create_current_datetime_filename(current_timestamp)}.csv"

    convert_data_csv_file(recordings_df, csv)

    s3 = client("s3",
                aws_access_key_id=ENV["AWS_ACCESS_KEY_ID"],
                aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    load_csv_file(s3, csv, ENV)
