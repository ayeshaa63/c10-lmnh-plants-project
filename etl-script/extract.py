"""A script to extract data in a JSON format from several API endpoints. 
The data should then be returned as a Dataframe."""

import pandas as pd
import requests


def extract(plant_range: int) -> list:

    plants = []

    for i in range(plant_range):
        response = requests.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{i}")

        plant = response.json()

        plants.append(plant)

    return plants


def to_dataframe():
    pass


if __name__ == "__main__":

    print(extract())
