"""A script to insert missing plant data into the database"""


from os import environ as ENV

import requests
from pymssql import connect, Connection
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


def get_plant_data(plant_id: int) -> dict:
    """Extracts json data from API endpoint for given plant id."""

    try:
        response = requests.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=5)

        data = response.json()
        data['plant_id'] = plant_id
        return data

    except Exception as err:
        return {'error': 'Cannot connect to the API.',
                'exception': err, 'plant_id': plant_id}


def insert_continent(continent: str, conn: Connection, config):
    """Insert data into the continent table of the database,
    if it doesn't already exist.
    Return the continent id."""
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
    return continent_id['continent_id']


def insert_country(country: str, continent_id: int, conn, config):
    """Insert data into the country table of the database,
    if it doesn't already exist.
    Return the country id."""
    with conn.cursor() as cur:
        cur.execute(
            f"""SELECT country_id from {config['SCHEMA_NAME']}.country
                    WHERE name = '{country}' 
                    AND continent_id = {continent_id}
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
    return country_id['country_id']


def insert_origin(origin: list, conn: Connection, config):
    """Insert data into the origin table of the database,
    if it doesn't already exist.
    Return the origin id."""
    long, lat, location, country, continent = origin
    continent = continent.split('/')[-1]
    location = location.replace('\'', '\"')
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
    return origin_id['origin_id']


def insert_plant(data: dict, conn: Connection, config, origin_id: int):
    """Insert data for a plant into the plant table of the database."""
    plant_id = data['plant_id']
    name = data['name'].replace('\'', '\"')
    if 'scientific_name' in data:
        scientific_name = data['scientific_name'][0].replace('\'', '\"')
    else:
        scientific_name = name
    with conn.cursor() as cur:
        cur.execute(f"""INSERT INTO {config['SCHEMA_NAME']}.plant
                        (plant_id, name, scientific_name, origin_id) VALUES
                        ({plant_id}, '{name}', '{scientific_name}', {origin_id})
                        """)
        conn.commit()


def insert_images():
    """Insert data about the images of a plant if exists and upload to database."""
    return None


def insert_botanist(botanist: dict, conn: Connection, config) -> None:
    """Insert data into the botanist table of the database."""
    name, phone, email = botanist['name'], botanist['phone'], botanist['email']
    with conn.cursor() as cur:
        cur.execute(f"""SELECT * from {config['SCHEMA_NAME']}.botanist
                    WHERE name='{name}'
                    AND phone='{phone}'
                    AND email='{email}'""")
        botanist_info = cur.fetchone()
        if not botanist_info:
            cur.execute(f"""INSERT INTO {config['SCHEMA_NAME']}.botanist
                        (name, phone, email) VALUES
                        ('{name}', '{phone}', '{email}')""")
            conn.commit()


def insert_plant_data(plant_dict: dict, conn: Connection, config):
    """Insert data into all relevant tables of the database for a single plant."""
    origin_id = insert_origin(plant_dict['origin_location'], conn, config)
    insert_plant(plant_dict, conn, config, origin_id)
    insert_images()
    insert_botanist(plant_dict['botanist'], conn, config)


def insert_missing_plant(plant_id, config):
    """Insert missing plant into database from specific id."""
    plant = get_plant_data(plant_id)
    if plant:
        with connect_to_db(config) as conn:
            insert_plant_data(plant, conn, config)
            return True
    else:
        return False


if __name__ == "__main__":
    load_dotenv()
    insert_missing_plant(45, ENV)
