"""
Filename: clear_register_passwordreset.py

Author: Aleesha Bunrith(z5371516)
Created: 12/04/2022

Description: pytest fixture for registering one user and requesting a password
             reset
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register_passwordreset(clear_register):
    """ clears any data stored in data_store and registers a user with the
    given information and requests a password reset """

    resp = requests.post(config.url + 'auth/passwordreset/request/v1', 
                         json={'email': 'abc@def.com'})
    assert resp.status_code == STATUS_OK
