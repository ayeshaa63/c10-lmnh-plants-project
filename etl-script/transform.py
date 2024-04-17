"""A script that will clean and process the Dataframe passed into it.
It will output a Dataframe."""

import re
import pandas as pd
import time
import asyncio
from os import environ as ENV
from dotenv import load_dotenv


from extract import get_all_plants
from email_alert import send_email

ERROR_NOT_FOUND = "plant not found"
ERROR_ON_LOAN = "plant on loan to another museum"
ERROR_NO_CONNECTION = "Cannot connect to the API."
ERROR_SENSOR_FAIL = "plant sensor fault"


def get_phone_number(number: str) -> str:
    """Changes phone numbers so they only have digits and brackets"""
    return re.sub(r'[^0-9()]', '', number)


def recording_information(plant: dict) -> dict:
    """extract the necessary data from the plant json"""

    if not plant:
        return plant

    email = plant.get('botanist').get('email')
    name = plant.get('botanist').get('name')
    phone = plant.get('botanist').get('phone')
    image = plant.get('images')
    if image:
        license_url = image.get('license_url')
        origin_url = image.get('original_url')
    else:
        license_url = None
        origin_url = None

    last_watered = plant.get('last_watered')
    plant_id = plant.get('plant_id')
    timestamp = plant.get('recording_taken')
    plant_name = plant.get('name')
    scientific_name = plant.get('scientific_name')

    if scientific_name:
        scientific_name = scientific_name[0]
    soil_moisture = plant.get('soil_moisture')
    temp = plant.get('temperature')

    df_row = {
        "email": email,
        "name": name,
        "phone": phone,
        "license_url": license_url,
        "origin_url": origin_url,
        "last_watered": last_watered,
        "plant_id": plant_id,
        "plant_name": plant_name,
        "timestamp": timestamp,
        "scientific_name": scientific_name,
        "soil_moisture": soil_moisture,
        "temp": temp
    }

    return df_row


def clean(plant_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalise the data"""

    plant_df['last_watered'] = plant_df['last_watered'].str.strip()
    plant_df['last_watered'] = pd.to_datetime(
        plant_df['last_watered'], format='%a, %d %b %Y %H:%M:%S %Z')
    plant_df['last_watered'] = plant_df['last_watered'].dt.tz_localize(None)
    plant_df['last_watered'] = plant_df['last_watered'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    plant_df['timestamp'] = pd.to_datetime(plant_df['timestamp'])
    plant_df['timestamp'] = plant_df['timestamp'].dt.tz_localize(None)
    plant_df['phone'] = plant_df['phone'].apply(get_phone_number)

    return plant_df


def error_handling(plant: dict) -> None:
    """A function to appropriately handle any errors from the api"""

    error_msg = 'ERROR :: PLANT {} :: {} :: {}'
    error_msg = error_msg.format(plant.get('plant_id'),
                                 plant.get('error'), plant.get('exception'))

    if plant.get('error') == ERROR_SENSOR_FAIL:
        return error_msg
    if plant.get('error') == ERROR_ON_LOAN:
        return ""

    print(error_msg)
    return ""


def transform(plants: list[dict]) -> pd.DataFrame:
    """main transforming function"""

    rows = []
    sensor_failures = []
    for plant in plants:
        if plant.get('error'):
            error_msg = error_handling(plant)
            if error_msg:
                sensor_failures.append(error_msg)
            continue
        rows.append(recording_information(plant))

    plant_df = pd.DataFrame(rows)

    if sensor_failures:
        send_email(sensor_failures)

    if rows:
        plant_df = clean(plant_df)
    return plant_df


if __name__ == "__main__":

    start_time = time.time()
    load_dotenv()
    plants = asyncio.run(get_all_plants(51))
    df = transform(plants)
    print(df)
    print(f"--- {(time.time() - start_time)} seconds taken ---")
