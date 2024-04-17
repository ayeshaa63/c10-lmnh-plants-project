import pandas as pd
import requests
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


def get_plant_data(plant_id: int) -> pd.DataFrame:
    '''Extracts json data from API endpoint for given plant id.'''

    try:
        response = requests.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=5)

        plant = response.json()

        return plant

    except Exception:
        return {'error': 'Cannot connect to the API.'}


def get_all_plants(no_of_plants: int) -> list[dict]:
    '''Puts all plant information into a dataframe.'''
    plants = []

    for i in range(no_of_plants):
        plant = get_plant_data(i)
        plants.append(plant)

    return plants


def insert_continent(continent, conn, config):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT continent_id from {config['SCHEMA_NAME']}.continent
                    WHERE name = '{continent}'
                    """)
        continent_id = cur.fetchone()
        if not continent_id:
            cur.execute(f"""INSERT INTO {config['SCHEMA_NAME']}.continent
                        (name) VALUES
                        ('{continent}')""")
            conn.commit()
            cur.execute(f"""SELECT continent_id FROM {config['SCHEMA_NAME']}.continent
                        WHERE name = '{continent}'
                        """)
            continent_id = cur.fetchone()
    return continent_id


def insert_country(country, continent_id, conn, config):
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT country_id from {config['SCHEMA_NAME']}.country
                    WHERE name = '{country}'
                    AND continent_id = '{continent_id}'
                    """)
        country_id = cur.fetchone()
        if not country_id:
            cur.execute(f"""INSERT INTO {config['SCHEMA_NAME']}.country
                        (name, continent_id) VALUES
                        ('{country}', {continent_id})""")
            conn.commit()
            cur.execute(f"""SELECT country_id FROM {config['SCHEMA_NAME']}.country
                        WHERE name = '{country}'
                        AND continent_id = {continent_id}
                        """)
            country_id = cur.fetchone()
    return country_id


def insert_origin(origin: list, conn: Connection, config):
    long, lat, location, country, continent = origin
    continent = continent.split('/')[-1]
    continent_id = insert_continent(continent, conn, config)
    country_id = insert_country(country, continent_id, conn, config)
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT origin_id from {config['SCHEMA_NAME']}.origin
                    WHERE long = {long}
                        AND lat = {lat}
                        AND location_name = '{location}'
                        AND country_id = {country_id}
                    """)
        origin_id = cur.fetchone()
        if not origin_id:
            cur.execute(f"""INSERT INTO {config['SCHEMA_NAME']}.origin
                        (long, lat, location_name, country_id) VALUES
                        ({long}, {lat}, '{location}', {country_id})
                        """)
            conn.commit()
            cur.execute(f"""SELECT origin_id FROM {config['SCHEMA_NAME']}.origin
                        WHERE long = {long}
                        AND lat = {lat}
                        AND location_name = '{location}'
                        AND country_id = {country_id}
                        """)
            origin_id = cur.fetchone()
    return origin_id


def insert_plant(data: dict, conn: Connection, config, origin_id):
    plant_id = data['plant_id']
    name = data['name']
    scientific_name = data['scientific_name']
    with conn.cursor() as cur:
        cur.execute(f"""INSERT INTO {config['SCHEMA_NAME']}.plant
                        (plant_id, name, scientific_name, origin_id) VALUES
                        ({plant_id}, '{name}', '{scientific_name}', {origin_id})
                        """)
        conn.commit()


def insert_images():
    pass


def insert_botanist():
    pass


def insert_plant_data(plant_dict: dict, conn, config):
    origin_id = insert_origin(plant_dict['origin_location'], conn, config)
    insert_plant(plant_dict, conn, config, origin_id)


def insert_metadata(data, config):
    with connect_to_db(config) as conn:
        for plant in data:
            insert_plant_data(plant, conn, config)


if __name__ == "__main__":
    load_dotenv()
    plants = get_all_plants(51)
    print(plants)
