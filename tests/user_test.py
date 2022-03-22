
import pytest
import json
from src.auth import auth_register_v1
from src.user import user_profile_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src import config

import requests


@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    requests.delete(config.url + 'clear/v1')
    user = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    user_json = user.json()
    return user_json


def test_user_profile(clear_and_register):
    """
    Create two users, 
    then call user_profile_v1, with the token as the first user,
    and the id of the second user.
    Returns the info of the ID given.
    """

    user0_json = clear_and_register
    user1 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'def@abc.com', 'password': 'password',
                        'name_first': 'first0', 'name_last': 'last0'})
    assert user1.status_code == 200
    user1_json = user1.json()

    # returns the info for the user_id given.
    #user_profile = user_profile_v1(user0['token'], user1_json['auth_user_id'])

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user1_json['token'], 'u_id': user0_json['auth_user_id']})
    assert user_profile.status_code == 200

    assert user_profile.json() == {
        'u_id': user0_json['auth_user_id'],
        'email': 'abc@def.com',
        'name_first': 'first',
        'name_last': 'last',
        'handle_str': 'firstlast',
    }


def test_profile_bad_input(clear_and_register):
    """
    Calls user_profile with:
        -   An invalid user_id, invalid token
        -   An invalid user_id, valid token
        -   A valid user_id, invalid token

    Arguments: 
        clear_and_register

    Exceptions: 
        InputError - Raised for all tests below

    Return Value: N/A
    """
    '''Testing with a bad token'''
    user_json = clear_and_register
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': '4444', 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400

    '''tesing with a bad user_id'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': 'bad_user_id'})
    assert user_profile.status_code == 500

    '''tesing with a bad token and user_id'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': 'bad_token', 'u_id': 'bad_user_id'})
    assert user_profile.status_code == 500
