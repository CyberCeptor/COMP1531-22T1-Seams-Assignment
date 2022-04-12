"""
Filename: auth_passwordreset_request_test.py

Author: Aleesha Bunrith(z5371516)
Created: 12/04/2022

Description: pytests for auth/passwordreset/request/v1
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.mark.usefixtures('clear_register')
def test_passwordreset_request_valid_email(clear_register):
    """ checks that a 200 status code is given """

    resp = requests.post(config.url + 'auth/passwordreset/request/v1', 
                         json={'email': 'abc@def.com'})
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register')
def test_passwordreset_request_invalid_email(clear_register):
    """ checks that a 200 status code is given even when email is invalid """

    resp = requests.post(config.url + 'auth/passwordreset/request/v1', 
                         json={'email': 'def@ghi.com'})
    assert resp.status_code == STATUS_OK

requests.delete(config.url + 'clear/v1')
