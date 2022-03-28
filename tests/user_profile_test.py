"""
Filename: user_profile_test.py

Author: Jenson Morgan(z5360181)
Created: 21/03/2022 - 27/03/2022

Description: pytests for user/profile/v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register_two')
def test_user_profile_working(clear_register_two):
    """ Create two users,
    then calls user_profile_v1 with the token of the first user,
    and the id of the second user.
    Returns the info of the ID given. (i.e., the second user) """

    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # user2 is looking at user1's profile
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user2['token'], 
                            'u_id': user1['auth_user_id']})
    assert user_profile.status_code == 200
    profile = user_profile.json()

    assert profile['user']['u_id'] == user1['auth_user_id']
    assert profile['user']['email'] == 'abc@def.com'
    assert profile['user']['name_first'] == 'first'
    assert profile['user']['name_last'] == 'last'
    assert profile['user']['handle_str'] == 'firstlast'

    # user1 is looking at their own profile
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user1['token'], 
                            'u_id': user1['auth_user_id']})
    assert user_profile.status_code == 200
    profile = user_profile.json()

    assert profile['user']['u_id'] == user1['auth_user_id']
    assert profile['user']['email'] == 'abc@def.com'
    assert profile['user']['name_first'] == 'first'
    assert profile['user']['name_last'] == 'last'
    assert profile['user']['handle_str'] == 'firstlast'

    # user2 is looking at their own profile
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user2['token'], 
                            'u_id': user2['auth_user_id']})
    assert user_profile.status_code == 200
    profile = user_profile.json()

    assert profile['user']['u_id'] == user2['auth_user_id']
    assert profile['user']['email'] == 'def@ghi.com'
    assert profile['user']['name_first'] == 'first'
    assert profile['user']['name_last'] == 'last'
    assert profile['user']['handle_str'] == 'firstlast0'

@pytest.mark.usefixtures('clear_register')
def test_profile_bad_token_input(clear_register):
    """ Calls user_profile with a bad token:
        -   a string
        -   an int
        -   a boolean
        -   an empty string
        -   an expired token
        -   an unsaved token """

    # Testing with a bad token
    user_json = clear_register
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': 'bad_token', 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403

    # tesing with a bad token as int
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': 4444, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400

    # tesing with a bad token as bool
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': True, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400

    # tesing with a bad token as an empty string
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': '', 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': expired_token, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': unsaved_token, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403

@pytest.mark.usefixtures('clear_register')
def test_profile_bad_u_id_input(clear_register):
    """ Calls user_profile with a bad user_id:
        -   an invalid user_id, not in the data_store
        -   a negative int
        -   a boolean
        -   an empty string
        -   a string """

    user_json = clear_register
    # tesing with a bad id as an int
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': 100})
    assert user_profile.status_code == 400

    # tesing with a bad id as a negative int
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': -100})
    assert user_profile.status_code == 400
    
    # tesing with a bad user_id as bool
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': True})
    assert user_profile.status_code == 400

    # tesing with a bad user_id as bool
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': False})
    assert user_profile.status_code == 400

    # tesing with a bad user_id as an empty string
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': ''})
    assert user_profile.status_code == 400

    # tesing with a bad user_id as a string
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': 'bad_user_id'})
    assert user_profile.status_code == 400

requests.delete(config.url + 'clear/v1')
