'''Tests functions in the extract file.'''

from unittest.mock import patch
import pandas as pd
from extract import get_dataframe


@patch('extract.get_plant_data')
def test_get_valid_dataframe(fake_get_plant, test_plant):
    '''Tests the function returns a pandas dataframe.'''

    fake_get_plant.return_value = test_plant
    fake_get_plant.status_code = 200

    plant = get_dataframe()

    assert isinstance(plant, pd.DataFrame) is True
