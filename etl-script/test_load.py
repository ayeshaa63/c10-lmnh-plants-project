"""Test the functions involved in the load file."""
from unittest.mock import patch
import pandas as pd
from load import get_botanist_ids, check_plants, upload_watering_data, upload_recordings_data, load


@patch("load.connect_to_db")
def test_load(fake_db_connection):
    """A test to pass the workflow checks (for now)"""
    fake_db_connection = None
    fake_db_connection.commit = None
    fake_db_connection.return_value.cursor.return_value = None
    fake_db_connection.return_value.cursor.return_value.execute.return_value = None
    fake_db_connection.return_value.cursor.return_value.fetchone.return_value = {
        'botanist_id': 1}
    fake_environ = {'SCHEMA_NAME': 'test_schema'}
    test_return = get_botanist_ids(pd.DataFrame({'name': ['mickey', 'mouse'], 'phone': [
        '8437234', '0-09280'], 'email': ['87324r832@gmail.com', 'mickeymouse@clubhouse.com']}), fake_db_connection, fake_environ)
    assert 'botanist_id' in test_return
    assert isinstance(test_return['botanist_id'].values[0], int)
    assert test_return == pd.DataFrame({'name': ['mickey', 'mouse'], 'phone': [
        '8437234', '0-09280'], 'email': ['87324r832@gmail.com', 'mickeymouse@clubhouse.com'], 'botanist_id': [1, 1]})
