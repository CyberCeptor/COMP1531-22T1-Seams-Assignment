"""
Filename: clear_and_register.py

Author: Aleesha Bunrith(z5371516)
Created: 26/03/2022

Description: pytest fixture for registering one user
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register():
    """ clears any data stored in data_store and registers a user with the
    given information and returns the json return info """

    requests.delete(config.url + 'clear/v1')

    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp.status_code == STATUS_OK
    user1 = resp.json()

    return user1
