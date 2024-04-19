from datetime import datetime
from os import environ as ENV

import pandas as pd
import pytest
from unittest.mock import MagicMock

from storage_load import create_current_datetime_key, get_old_recordings


def test_create_current_datetime_key(sample_datetime1):
    assert create_current_datetime_key(
        sample_datetime1) == "2000/11/29/14:48"


def test_create_current_datetime_key_single_digit_entries(sample_datetime2):
    assert create_current_datetime_key(sample_datetime2) == "2000/1/1/00:00"


def test_get_old_recordings(sample_datetime_older_than_24_hrs):

    mock_connection = MagicMock()

    mock_fetch = mock_connection.cursor().__enter__().fetchall

    mock_fetch.return_value = [{'recording_id': 1, 'timestamp':
                                sample_datetime_older_than_24_hrs,
                                'temp': 10.0, 'soil_moisture': 11.0, 'botanist_id': 1,
                                'plant_id': 1},
                               {'recording_id': 2, 'timestamp': datetime.now(),
                                'temp': 10.0, 'soil_moisture': 11.0, 'botanist_id': 1,
                                'plant_id': 2}]

    fake_environ = {'SCHEMA_NAME': 'test_schema'}

    assert isinstance(get_old_recordings(
        mock_connection, fake_environ), pd.DataFrame) == True
