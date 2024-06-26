"""Test the functions involved in the load file."""
from unittest.mock import patch, MagicMock
import pandas as pd
from load import get_botanist_ids, check_plants, upload_watering_data, upload_recordings_data, load


def test_botanist_func_valid():
    """Test that the function 'get_botanist_ids' runs correctly."""
    mock_connect = MagicMock()
    cursor = mock_connect.cursor.return_value
    cursor.__enter__.return_value.fetchone.return_value = {'botanist_id': 1}
    fake_environ = {'SCHEMA_NAME': 'test_schema'}
    test_return = get_botanist_ids(pd.DataFrame({'name': ['mickey', 'mouse'], 'phone': [
        '8437234', '0-09280'], 'email': ['87324r832@gmail.com', 'mickeymouse@clubhouse.com']}), mock_connect, fake_environ)
    assert isinstance(test_return, pd.DataFrame)
    assert 'botanist_id' in test_return
    assert 'name' in test_return
    assert 'phone' in test_return
    assert 'email' in test_return
    assert pd.api.types.is_numeric_dtype(test_return['botanist_id'])
