"""Pytest fixtures for test files."""
import pytest


@pytest.fixture
def test_single_full_json():
    """A single plant recording with everything in it"""
    return {'botanist':
            {'email': 'carl.linnaeus@lnhm.co.uk',
             'name': 'Carl Linnaeus', 'phone': '(146)994-1635x35992'},
            'images': {'license': 45, 'license_name': 'Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)',
                       'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/deed.en',
                       'medium_url': 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/medium/2560px-Epipremnum_aureum_31082012.jpg',
                       'original_url': 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/og/2560px-Epipremnum_aureum_31082012.jpg',
                       'regular_url': 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/regular/2560px-Epipremnum_aureum_31082012.jpg',
                       'small_url': 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/small/2560px-Epipremnum_aureum_31082012.jpg',
                       'thumbnail': 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/thumbnail/2560px-Epipremnum_aureum_31082012.jpg'},
            'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT', 'name': 'Epipremnum Aureum',
            'origin_location': ['-19.32556', '-41.25528', 'Resplendor', 'BR', 'America/Sao_Paulo'],
            'plant_id': 0, 'recording_taken': '2024-04-16 08:22:43',
            'scientific_name': ['Epipremnum aureum'],
            'soil_moisture': 36.12849992449178,
            'temperature': 22.187149686325654}


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


def test_expected_outcome_full_single():
    """The expected output of the full plant record"""
    return {'email': 'carl.linnaeus@lnhm.co.uk',
            'name': 'Carl Linnaeus',
            'phone': '(146)994-1635x35992',
            'license_url': 'https://creativecommons.org/licenses/by-sa/3.0/deed.en',
            'origin_url': 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/og/2560px-Epipremnum_aureum_31082012.jpg',
            'last_watered': 'Mon, 15 Apr 2024 14:03:04 GMT',
            'plant_id': 0,
            'timestamp': '2024-04-16 08:22:43',
            'scientific_name': 'Epipremnum aureum',
            'soil_moisture': 36.12849992449178,
            'temp': 22.187149686325654}
