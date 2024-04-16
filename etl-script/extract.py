"""A script to extract data in a JSON format from several API endpoints. 
The data should then be returned as a Dataframe."""

import pandas as pd
import requests

NO_OF_PLANTS = 60


def get_plant_data(plant_id: int) -> pd.DataFrame:
    '''Extracts json data from API endpoint for given plant id.'''

    try:
        response = requests.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=5)

        plant = response.json()

        return plant

    except Exception:
        return {'error': 'Cannot connect to the API.'}


def get_dataframe() -> pd.DataFrame:
    '''Puts all plant information into a dataframe.'''
    plants = []

    for i in range(1, 10):
        plant = get_plant_data(i)
        plants.append(plant)

    return pd.DataFrame.from_dict(plants)


if __name__ == "__main__":

    get_dataframe()
