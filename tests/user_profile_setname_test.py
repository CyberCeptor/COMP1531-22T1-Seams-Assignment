"""
Filename: user_profile_setname_test.py

Author: Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: pytests for user_profile_setname__v1
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
                        'name_first': 'first', 'name_last': 'last'})
    user_data = user.json()
    token = user_data['token']

    return [token]

def test_user_profile_setname_bad_name_first(clear_and_register):
    token = clear_and_register[0]

    # test users name_first
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 200

    # test empty string
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': '', 'name_last': 'last'})
    assert setname.status_code == 400

    # test boolean 
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': True, 'name_last': 'last'})
    assert setname.status_code == 400

    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': False, 'name_last': 'last'})
    assert setname.status_code == 400

    # test < 1 int
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 0, 'name_last': 'last'})
    assert setname.status_code == 400

    # test > 50 int
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 51, 'name_last': 'last'})
    assert setname.status_code == 400

    requests.delete(config.url + 'clear/v1')


def test_user_profile_setname_bad_name_last(clear_and_register):
    token = clear_and_register[0]

    # test another users name_last
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 200

    # test empty string
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': ''})
    assert setname.status_code == 400

    # test boolean 
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': True})
    assert setname.status_code == 400

    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': False})
    assert setname.status_code == 400

    # test < 1 int
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': 0})
    assert setname.status_code == 400

    # test > 50 int
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': token, 'name_first': 'first', 'name_last': 51})
    assert setname.status_code == 400

    requests.delete(config.url + 'clear/v1')