"""
Filename: user_profile_sethandle_test.py

Author: Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: pytests for user_profile_sethandle_v1
"""

import pytest
import requests
from src import config

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: user_data in json form.
    """
    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last', 'handle_str': 'handle'})
    user_data = user.json()
    token = user_data['token']
    handle_str = user_data['handle_str']

    return [token, handle_str]

def test_user_profile_sethandle_bad_handle_str(clear_and_register):
    token = clear_and_register[0]

    # test users handle_str
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': 'handle'})
    assert sethandle.status_code == 400

    # test not alphanumeric handle_str
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': ' '})
    assert sethandle.status_code == 400

    # test empty string
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': ''})
    assert sethandle.status_code == 400

    # test boolean 
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': True})
    assert sethandle.status_code == 400

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': False})
    assert sethandle.status_code == 400

    # test < 3 int
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': 2})
    assert sethandle.status_code == 400

    # test > 20 int
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': token, 'handle_str': 21})
    assert sethandle.status_code == 400

    requests.delete(config.url + 'clear/v1')
