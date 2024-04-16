'''Pytest fixtures for test file.'''
import pytest


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
