"""A script to extract data in a JSON format from several API endpoints. 
The data should then be returned as a Dataframe."""

import pandas as pd
import asyncio
import aiohttp
from datetime import datetime


async def get_plant_data(session, plant_id: int) -> pd.DataFrame:
    '''Extracts json data from API endpoint for given plant id.'''

    try:
        response = await session.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", timeout=20)

        data = await response.json()

        data['plant_id'] = plant_id

        return data

    except Exception as e:
        return {'error': 'Cannot connect to the API.',
                'exception': e}


async def get_all_plants(no_of_plants: int) -> list[dict]:
    '''Returns a list of plants along with their data.'''

    async with aiohttp.ClientSession() as session:
        tasks = []

        for i in range(no_of_plants):
            tasks.append(get_plant_data(session, i))

        return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":

    resp = asyncio.run(get_all_plants(51))

