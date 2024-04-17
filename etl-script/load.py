"""Take the Dataframe returned from transform.py and
upload it to a Microsoft SQL Server database."""

import pandas as pd
from pymssql import connect, Connection
from os import environ as ENV
from dotenv import load_dotenv


def connect_to_db(config):
    """Returns a live database connection."""
    return connect(
        server=config["DB_HOST"],
        user=config["DB_USER"],
        password=config["DB_PASS"],
        database=config["DB_NAME"],
        port=config["DB_PORT"],
        as_dict=True
    )


def get_botanist_ids(df: pd.DataFrame, conn: Connection, config) -> pd.DataFrame:
    """Look through botanist data in database:
     - If botanist doesn't exist, add them to database and get id,
     - If botanist does already exist, get their id as appear in table.
     Replace botanist columns in DataFrame to a column of ids."""
    botanists = df[['name', 'phone', 'email']].drop_duplicates()
    ids = []

    with conn.cursor() as cur:
        for _, botanist in botanists.iterrows():
            cur.execute(
                f"""SELECT * from {config['SCHEMA_NAME']}.botanist
                    WHERE name='{botanist.iloc[0]}'
                    AND phone='{botanist.iloc[1]}'
                    AND email='{botanist.iloc[2]}'""")
            botanist_info = cur.fetchone()
            if not botanist_info:
                cur.execute(
                    f"""INSERT INTO {config['SCHEMA_NAME']}.botanist
                        (name, phone, email) VALUES
                        ('{botanist.iloc[0]}', '{botanist.iloc[1]}', '{botanist.iloc[2]}')""")
                conn.commit()
                cur.execute(
                    f"""SELECT * from {config['SCHEMA_NAME']}.botanist
                    WHERE name='{botanist.iloc[0]}'
                    AND phone='{botanist.iloc[1]}'
                    AND email='{botanist.iloc[2]}'""")
                botanist_info = cur.fetchone()
            ids.append(botanist_info['botanist_id'])
    df['botanist_id'] = pd.Series(ids)
    return df


def upload_watering_data(df: pd.DataFrame, conn: Connection, config):
    """Upload new watering data to database."""
    # Not sure if to_sql will work yet, use INSERT INTO if not.
    waterings = df[['last_watered', 'plant_id']]
    with conn.cursor() as cur:
        for _, watering in waterings.iterrows():
            cmd = f"""IF NOT EXISTS (SELECT timestamp, plant_id
                        FROM {config['SCHEMA_NAME']}.watering
                        WHERE timestamp = CAST('{watering.iloc[0]}' AS DATETIME)
                        AND plant_id = {watering.iloc[1]})
                        BEGIN
                        INSERT INTO {config['SCHEMA_NAME']}.watering
                        (timestamp, plant_id) VALUES
                        (CAST('{watering.iloc[0]}' AS DATETIME), {watering.iloc[1]})
                        END"""
            print(cmd)
            cur.execute(cmd)
            # f"""INSERT INTO {config['SCHEMA_NAME']}.watering
            #     (timestamp, plant_id) VALUES
            #     ('{watering.iloc[0]}', '{watering.iloc[1]}')
            #     WHERE NOT EXISTS (
            #     SELECT timestamp, plant_id FROM {config['SCHEMA_NAME']}.watering
            #     WHERE timestamp = {watering.iloc[0]}
            #     AND plant_id = {watering.iloc[1]}
            #     )""")

            conn.commit()


def upload_recordings_data(df: pd.DataFrame, conn: Connection, config):
    """Uploads transaction data to the database."""
    # Not sure if to_sql will work yet, use INSERT INTO if not.
    recordings = df[['timestamp', 'temp',
                     'soil_moisture', 'botanist_id', 'plant_id']]
    with conn.cursor() as cur:
        for _, record in recordings.iterrows():
            cur.execute(
                f"""INSERT INTO {config['SCHEMA_NAME']}.recordings
                    (timestamp, temp, soil_moisture, botanist_id, plant_id) VALUES
                    ('{record.iloc[0]}', '{record.iloc[1]}', '{record.iloc[2]}', '{record.iloc[3]}', '{record.iloc[4]}')
                    )""")

            conn.commit()


def load(df: pd.DataFrame) -> None:
    """main load function"""
    with connect_to_db(ENV) as conn:
        df = get_botanist_ids(df, conn, ENV)
        upload_watering_data(df, conn, ENV)
        upload_recordings_data(df, conn, ENV)


if __name__ == "__main__":
    load_dotenv()
    # load(pd.DataFrame({'name': ['mickey', 'mickey', 'mouse'], 'phone': [
    #     '839429', '839429', '4872682'], 'email': ['mickeymouse@clubhouse.com', 'mickeymouse@clubhouse.com', 'anemail@email.com']}))
    load(pd.DataFrame({"email": ['mickeymouse@clubhouse.com'],
                      "name": ['mickey'],
                       "phone": '666',
                       "license_url": 'license_url',
                       "origin_url": 'origin_url',
                       "last_watered": pd.to_datetime('01/01/2024'),
                       "plant_id": 5,
                       "timestamp": pd.to_datetime('01/01/2024'),
                       "soil_moisture": 2.0,
                       "temp": 3.0}))
