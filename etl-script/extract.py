"""A script to extract data in a JSON format from several API endpoints. 
The data should then be returned as a Dataframe."""

import pandas as pd
import requests
import multiprocessing


def get_plant_data(plant_id: int) -> pd.DataFrame:
    '''Extracts json data from API endpoint for given plant id.'''

    try:
        response = requests.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=10)

        plant = response.json()

        return plant

    except Exception as e:
        return {'error': 'Cannot connect to the API.',
                'exception': e}


def get_all_plants(no_of_plants: int) -> list[dict]:
    '''Returns a list of plants along with their data.'''
    pool_obj = multiprocessing.Pool()

    with pool_obj as p:
        ans = p.map(get_plant_data, range(0, no_of_plants))
        return ans


if __name__ == "__main__":

    get_all_plants(51)
