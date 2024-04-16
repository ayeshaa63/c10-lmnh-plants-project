"""A script that will clean and process the Dataframe passed into it.
It will output a Dataframe."""

import re
import pandas as pd


def get_phone_number(num):
    """Changes phone numbers so they only have digits and brackets"""
    return re.sub(r'[^0-9()]', '', num)


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
        "timestamp": timestamp,
        "scientific_name": scientific_name,
        "soil_moisture": soil_moisture,
        "temp": temp
    }

    print(df_row)
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


def transform(plants: list[dict]) -> pd.DataFrame:
    """main transforming function"""

    rows = []
    for plant in plants:
        rows.append(recording_information(plant))
    plant_df = pd.DataFrame(rows)
    plant_df = clean(plant_df)
    return plant_df
