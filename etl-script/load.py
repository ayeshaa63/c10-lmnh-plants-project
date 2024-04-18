"""Take the Dataframe returned from transform.py and
upload it to a Microsoft SQL Server database."""

import asyncio
import time
from os import environ as ENV

import pandas as pd
from pymssql import connect, Connection
from dotenv import load_dotenv

from extract import get_all_plants
from transform import transform
from insert_missing_metadata import insert_missing_plant


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


def get_botanist_ids(dataframe: pd.DataFrame, conn: Connection, config) -> pd.DataFrame:
    """Look through botanist data in database:
     - If botanist doesn't exist, add them to database and get id,
     - If botanist does already exist, get their id as appear in table.
     Replace botanist columns in DataFrame to a column of ids."""
    botanists = dataframe[['name', 'phone', 'email']]
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
    dataframe['botanist_id'] = pd.Series(ids, dtype=int)
    return dataframe


def check_plants(dataframe: pd.DataFrame, conn: Connection, config):
    """Insert data for a plant into the plant table of the database."""
    plants = dataframe[[
        "plant_id",
        "scientific_name",
        "soil_moisture",
        "temp"]]
    bad_plants = []
    with conn.cursor() as cur:
        for _, plant in plants.iterrows():
            plant_id = plant.iloc[0]
            cur.execute(
                f"""SELECT * from {config['SCHEMA_NAME']}.plant
                    WHERE plant_id = {plant_id}
                    """)
            plant_info = cur.fetchone()
            if not plant_info:
                try:
                    insert_missing_plant(plant_id, ENV)
                except Exception:
                    bad_plants.append(plant_id)
    return bad_plants


def upload_watering_data(dataframe: pd.DataFrame, conn: Connection, config, bad_plants):
    """Upload new watering data to database."""
    waterings = dataframe[['last_watered', 'plant_id']]
    with conn.cursor() as cur:
        for _, watering in waterings.iterrows():
            if watering.iloc[1] not in bad_plants:
                cur.execute(f"""IF NOT EXISTS (SELECT timestamp, plant_id
                        FROM {config['SCHEMA_NAME']}.watering
                        WHERE timestamp = '{watering.iloc[0]}'
                        AND plant_id = {int(watering.iloc[1])})
                        BEGIN
                        INSERT INTO {config['SCHEMA_NAME']}.watering
                        (timestamp, plant_id) VALUES
                        ('{watering.iloc[0]}', {int(watering.iloc[1])})
                        END""")
                conn.commit()
            else:
                print(f"Plant {watering.iloc[1]} isn't in the database!")


def upload_recordings_data(dataframe: pd.DataFrame, conn: Connection, config, bad_plants):
    """Uploads transaction data to the database."""
    recordings = dataframe[['timestamp', 'temp',
                            'soil_moisture', 'botanist_id', 'plant_id']]
    with conn.cursor() as cur:
        for _, record in recordings.iterrows():
            if record.iloc[4] not in bad_plants:
                cur.execute(
                    f"""INSERT INTO {config['SCHEMA_NAME']}.recording
                        (timestamp, temp, soil_moisture, botanist_id, plant_id) VALUES
                        ('{record.iloc[0]}', '{record.iloc[1]}', '{record.iloc[2]}', '{int(record.iloc[3])}', '{int(record.iloc[4])}')
                        """)

                conn.commit()
            else:
                print(f"Plant {record.iloc[4]} isn't in the database!")


def load(dataframe: pd.DataFrame, config) -> None:
    """Load new records into database."""
    with connect_to_db(config) as conn:
        bad_plants = check_plants(dataframe, conn, config)
        dataframe = get_botanist_ids(dataframe, conn, config)
        upload_watering_data(dataframe, conn, config, bad_plants)
        upload_recordings_data(dataframe, conn, config, bad_plants)


def handler(event=None, context=None):
    '''Lambda handler function'''
    load_dotenv()
    all_plants = asyncio.run(get_all_plants(51))
    data = transform(all_plants)
    load(data, ENV)


if __name__ == "__main__":
    load_dotenv()
    start_time = time.time()
    all_plants = asyncio.run(get_all_plants(51))
    data = transform(all_plants)
    load(data, ENV)
    print(f"--- {(time.time() - start_time)} seconds taken ---")
