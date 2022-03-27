"""
Filename: clear_register_two.py

Author: Aleesha Bunrith(z5371516)
Created: 26/03/2022

Description: pytest fixture for registering two users
"""

import pytest

import requests

from src import config

@pytest.fixture
def clear_register_two(clear_register):
    """ clears any data stored in data_store and registers two users with the
    given information and returns the json return info for each """

    user1 = clear_register

    resp = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first2', 'name_last': 'last2'})
    assert resp.status_code == 200
    user2 = resp.json()

    return [user1, user2]
