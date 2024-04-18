from datetime import datetime
import pandas as pd
import pytest

from storage_load import create_current_datetime_filename


@pytest.fixture
def sample_datetime():
    return datetime(year=2000, month=11, day=29, hour=14, minute=48)


def test_create_current_datetime_filename(sample_datetime):
    assert create_current_datetime_filename(
        sample_datetime) == "2000/11/29/14:48"
