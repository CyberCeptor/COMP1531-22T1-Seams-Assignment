"""
Filename: clear_and_register_two.py

Author: Aleesha Bunrith(z5371516)
Created: 26/03/2022

Description: pytest fixture for creating two users
"""

import pytest

import requests

from src import config

@pytest.fixture
def clear_and_register_two():
    """ clears any data stored in data_store and registers two users with the
    given information and returns the json return info for each """

    requests.delete(config.url + 'clear/v1')

    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user1 = resp0.json()

    resp1 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 200
    user2 = resp1.json()

    return [user1, user2]
