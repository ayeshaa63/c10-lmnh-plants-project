
"""Pytest fixtures for test files."""

import pytest


@pytest.fixture
def test_single_full_json():
    """A single plant recording with everything in it"""
    return {'botanist':
            {'email': 'carl.linnaeus@lnhm.co.uk',
             'name': 'Carl Linnaeus', 'phone': '(146)994-1635x35992'},
            'images': {'license': 45, 'license_name': 'Attribution-ShareAlike 3.0 Unported',
                       'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/deed.en',
                       'medium_url': 'https://perenual.com/medium/Epipremnum_aureum.jpg',
                       'original_url': 'https://perenual.com/og/Epipremnum_aureum.jpg',
                       'regular_url': 'https://perenual.com/regular/Epipremnum_aureum.jpg',
                       'small_url': 'https://perenual.com/small/Epipremnum_aureum.jpg',
                       'thumbnail': 'https://perenual.com/thumbnail/Epipremnum_aureum.jpg'},
            'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'name': 'Epipremnum Aureum',
            'origin_location': ['-19.32556', '-41.25528', 'Resplendor', 'BR', 'America/Sao_Paulo'],
            'plant_id': 0, 'recording_taken': '2024-04-16 08:22:43',
            'scientific_name': ['Epipremnum aureum'],
            'soil_moisture': 36.12849992449178,
            'temperature': 22.187149686325654}


@pytest.fixture
def test_single_record_no_image_scientific_name():
    """a single plant record but with no image or scientific name"""
    return {'botanist':
            {'email': 'carl.linnaeus@lnhm.co.uk',
             'name': 'Carl Linnaeus', 'phone': '(146)994-1635x35992'},
            'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'name': 'Epipremnum Aureum',
            'origin_location': ['-19.32556', '-41.25528', 'Resplendor', 'BR', 'America/Sao_Paulo'],
            'plant_id': 0, 'recording_taken': '2024-04-16 08:22:43',
            'soil_moisture': 36.12849992449178,
            'temperature': 22.187149686325654}


@pytest.fixture
def test_expected_outcome_full_single():
    """The expected output of the full plant record"""
    return {'email': 'carl.linnaeus@lnhm.co.uk',
            'name': 'Carl Linnaeus',
            'phone': '(146)994-1635x35992',
            'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/deed.en',
            'origin_url': 'https://perenual.com/og/Epipremnum_aureum.jpg',
            'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT',
            'plant_id': 0,
            'plant_name': 'Epipremnum Aureum',
            'timestamp': '2024-04-16 08:22:43',
            'scientific_name': 'Epipremnum aureum',
            'soil_moisture': 36.12849992449178,
            'temp': 22.187149686325654}


@pytest.fixture
def test_plant():
    '''Returns an example dictionary.'''
    return {'botanist': {'email': 'eliza.andrews@lnhm.co.uk',
                         'name': 'Eliza Andrews',
                         'phone': '(846)669-6651x75948'},
            'last_watered': 'Mon, 15 Apr 2024 14:50:16 GMT',
            'name': 'Rafflesia arnoldii',
            'origin_location': ['-19.32556', '-41.25528', 'Resplendor', 'BR', 'America/Sao_Paulo'],
            'plant_id': 3,
            'recording_taken': '2024-04-16 09:16:20',
            'soil_moisture': 36.24902002881845,
            'temperature': 9.975278583615802}
