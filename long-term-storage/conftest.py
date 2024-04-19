from datetime import datetime

import pytest

@pytest.fixture
def sample_datetime1():
    return datetime(year=2000, month=11, day=29, hour=14, minute=48)


@pytest.fixture
def sample_datetime2():
    return datetime(year=2000, month=1, day=1, hour=00, minute=00)


@pytest.fixture
def sample_datetime_older_than_24_hrs():
    return datetime(year=2024, month=4, day=18, hour=1, minute=1)
