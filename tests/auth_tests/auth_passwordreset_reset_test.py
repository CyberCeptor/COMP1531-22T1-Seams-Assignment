"""
Filename: auth_passwordreset_reset_test.py

Author: Aleesha Bunrith(z5371516)
Created: 12/04/2022

Description: pytests for auth/passwordreset/reset/v1
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_passwordreset')
def test_passwordreset_reset_invalid_reset_code_and_pw(clear_register_passwordreset):
    """ checks that errors are raised when invalid reset codes and invalid 
    passwords are given """

    # password is an empty str
    resp0 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': '-1', 
                               'new_password': ''})
    assert resp0.status_code == STATUS_INPUT_ERR

    # password is too short
    resp1 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': '-1', 
                               'new_password': 'pass'})
    assert resp1.status_code == STATUS_INPUT_ERR

    # password is an int
    resp2 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': '-1', 
                               'new_password': 1})
    assert resp2.status_code == STATUS_INPUT_ERR

    # password is a bool
    resp3 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': '-1', 
                               'new_password': True})
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_passwordreset')
def test_passwordreset_request_invalid_reset_code(clear_register_passwordreset):
    """ checks that errors are not raised when invalid reset codes are given """

    # code is a str of a negative number
    resp0 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': '-1', 
                               'new_password': 'password'})
    assert resp0.status_code == STATUS_INPUT_ERR

    # code is an empty str
    resp1 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': '', 
                               'new_password': 'password'})
    assert resp1.status_code == STATUS_INPUT_ERR

    # code is a bool
    resp2 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': True, 
                               'new_password': 'password'})
    assert resp2.status_code == STATUS_INPUT_ERR

    # code is an int
    resp3 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': 1, 
                               'new_password': 'password'})
    assert resp3.status_code == STATUS_INPUT_ERR

    # code is None
    resp3 = requests.post(config.url + 'auth/passwordreset/reset/v1', 
                         json={'reset_code': None, 
                               'new_password': 'password'})
    assert resp3.status_code == STATUS_INPUT_ERR

requests.delete(config.url + 'clear/v1')
