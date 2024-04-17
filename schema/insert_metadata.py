import pandas as pd
import requests
from pymssql import connect, Connection


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


def insert_continent():
    pass


def insert_country():
    pass


def insert_origin(origin: list):
    lat, long, location, country, continent = origin
    insert_continent(continent)
    insert_country(country)


def insert_plant():
    pass


def insert_images():
    pass


def insert_botanist():
    pass


def insert_plant_data(plant_dict: dict):
    insert_origin(plant_dict['origin_location'])


def insert_metadata(data):
    for plant in data:
        insert_plant_data(plant)


if __name__ == "__main__":

    plants = get_all_plants(51)
    print(plants)
