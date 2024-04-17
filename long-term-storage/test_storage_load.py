from boto3 import client
from dotenv import load_dotenv
import pandas as pd
import pymssql
import pytest

from storage_load import find_row_index_most_sim


@pytest.fixture
def big_series_sample():
    return pd.DataFrame({'temp': [10, 12, 15, 17, 21],
                         'soil_moisture': [0, 0, 0, 0, 0]
                         })


def test_find_row_index_most_sim():
    assert find_row_index_most_sim(big_series_sample) == 2
