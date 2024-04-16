'''Tests functions in the extract file.'''

from unittest.mock import patch
import pandas as pd
from extract import get_all_plants


@patch('extract.get_plant_data')
def test_get_valid_list(fake_get_plant, test_plant):
    '''Tests the function returns a list of dictionaries.'''

    fake_get_plant.return_value = test_plant
    fake_get_plant.status_code = 200

    plant = get_all_plants(60)

    assert isinstance(plant, list) is True
    assert isinstance(plant[0], dict) is True
