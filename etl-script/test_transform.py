"""Testing for the transform script."""

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from transform import get_phone_number, recording_information, transform, clean


@pytest.mark.parametrize("test_input,expected",
                         [("(012) 1234x12", "(012)123412"),
                          ("123s45mkds     678", "12345678"),
                          ("(146)994-1635x35992", "(146)994163535992")])
def test_phone_number(test_input, expected):
    """test the phone number extraction regex"""
    assert get_phone_number(test_input) == expected


def test_recording_information(test_single_full_json,
                               test_expected_outcome_full_single):
    """test a full json message"""

    expected_outcome = test_expected_outcome_full_single

    assert recording_information(test_single_full_json) == expected_outcome


def test_recording_information_empty():
    """Tests with a missing json entry and should return an empty"""
    assert not recording_information({})


def test_recording_information_missing_image_and_sname():
    """Tests a json data entry that is missing data 
    for the image and the scientific name"""
    test_data = {'botanist':
                 {'email': 'carl.linnaeus@lnhm.co.uk',
                     'name': 'Carl Linnaeus', 'phone': '(146)994-1635x35992'},
                 'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'name': 'Epipremnum Aureum',
                 'origin_location': ['-19.32556', '-41.25528',
                                     'Resplendor', 'BR', 'America/Sao_Paulo'],
                 'plant_id': 0, 'recording_taken': '2024-04-16 08:22:43',
                 'soil_moisture': 36.12849992449178,
                 'temperature': 22.187149686325654}

    expected_outcome = {'email': 'carl.linnaeus@lnhm.co.uk',
                        'name': 'Carl Linnaeus',
                        'phone': '(146)994-1635x35992',
                        'license_url': None,
                        'origin_url': None,
                        'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT',
                        'plant_id': 0,
                        "plant_name": 'Epipremnum Aureum',
                        'timestamp': '2024-04-16 08:22:43',
                        'scientific_name': None,
                        'soil_moisture': 36.12849992449178,
                        'temp': 22.187149686325654}

    assert recording_information(test_data) == expected_outcome


def test_transform(test_single_full_json,
                   test_expected_outcome_full_single):
    """Test the the transform script with one data entry"""

    expected_outcome = test_expected_outcome_full_single
    expected_outcome['phone'] = '(146)994163535992'

    expected_outcome = pd.DataFrame([expected_outcome])
    expected_outcome['last_watered'] = expected_outcome['last_watered'].str.strip()
    expected_outcome['last_watered'] = pd.to_datetime(
        expected_outcome['last_watered'], format='%a, %d %b %Y %H:%M:%S %Z')
    expected_outcome['last_watered'] = expected_outcome['last_watered'].dt.tz_localize(
        None)
    expected_outcome['last_watered'] = expected_outcome['last_watered'].dt.strftime(
        '%Y-%m-%d %H:%M:%S')
    expected_outcome['timestamp'] = pd.to_datetime(
        expected_outcome['timestamp'])

    actual_outcome = transform([test_single_full_json])

    assert isinstance(actual_outcome, pd.DataFrame)
    assert isinstance(expected_outcome, pd.DataFrame)
    assert_frame_equal(actual_outcome, expected_outcome)


def test_transform_empty():
    """test transform with an empty list"""
    actual_outcome = transform([])

    assert isinstance(actual_outcome, pd.DataFrame)


def test_transform_error(test_single_full_json, ):
    """test transform with an error value """
    actual_outcome = transform(
        [{'error': 'Cannot connect to the API.'}, test_single_full_json])

    assert isinstance(actual_outcome, pd.DataFrame)
    assert len(actual_outcome.index) == 1


def test_clean_negative_moisture():
    """Test that any plants with a erroneously negative soil moisture dont get through"""

    test_data = [{'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'timestamp': '2024-04-16 08:22:43',
                 'phone': '(146)994163535992', 'soil_moisture': -0.4566, 'temp': 22.187149686325654}]
    test_data = pd.DataFrame(test_data)

    actual_outcome = clean(test_data)

    assert isinstance(actual_outcome, pd.DataFrame)
    assert len(actual_outcome.index) == 0


def test_clean_negative_temp():
    """Test that any plants with a erroneously negative temperatures dont get through"""

    test_data = [{'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'timestamp': '2024-04-16 08:22:43',
                 'phone': '(146)994163535992', 'soil_moisture': 3.4566, 'temp': -0.187149686325654}]
    test_data = pd.DataFrame(test_data)

    actual_outcome = clean(test_data)

    assert isinstance(actual_outcome, pd.DataFrame)
    assert len(actual_outcome.index) == 0


def test_clean_high_moisture():
    """Test that any plants with a erroneously high soil moisture dont get through"""

    test_data = [{'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'timestamp': '2024-04-16 08:22:43',
                 'phone': '(146)994163535992', 'soil_moisture': 101.4566, 'temp': 22.187149686325654}]
    test_data = pd.DataFrame(test_data)

    actual_outcome = clean(test_data)

    assert isinstance(actual_outcome, pd.DataFrame)
    assert len(actual_outcome.index) == 0


def test_clean_high_temp():
    """Test that any plants with a erroneously high temperature dont get through"""

    test_data = [{'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'timestamp': '2024-04-16 08:22:43',
                 'phone': '(146)994163535992', 'soil_moisture': 33.4566, 'temp': 55.187149686325654}]
    test_data = pd.DataFrame(test_data)

    actual_outcome = clean(test_data)

    assert isinstance(actual_outcome, pd.DataFrame)
    assert len(actual_outcome.index) == 0
