"""
Filename: auth_handle_test.py

Author: Aleesha Bunrith(z5371516)
Created: 09/03/2022 - 27/03/2022

Description: pytests for handle generation from auth/register/v1
"""

import pytest

import requests

from src import config

name_22_chars = 'abcdefghijklmnopqrstuv'

@pytest.mark.usefixtures('clear_register')
def test_create_handle_duplicate(clear_register):
    """ testing if users/all returns the right handle values when there are
    two users with the same first and last name """
    
    token = clear_register['token']

    # register a second user with the same name
    resp0 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'def@ghi.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200

    # use users/all to get all user info
    resp1 = requests.get(config.url + 'users/all/v1', params={'token': token})
    assert resp1.status_code == 200
    get = resp1.json()

    # user1's handle will have no changes but user2's handle will have a digit
    # at the end
    assert get['users'][0]['handle_str'] == 'firstlast'
    assert get['users'][1]['handle_str'] == 'firstlast0'

def test_create_handle_longer_than_twenty():
    """ testing if users/all returns the right handle values when there are
    users with a name longer than 20 characters """

    requests.delete(config.url + 'clear/v1')

    # create a user with a first name longer than 20 characters
    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': name_22_chars,
                               'name_last': 'last'})
    assert resp0.status_code == 200
    user1 = resp0.json()
    token = user1['token']

    # create a second user with a last name longer than 20 characters
    resp1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first',
                               'name_last': name_22_chars})
    assert resp1.status_code == 200

    # create a third user with a full name longer than 20 characters
    resp2 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'ghi@jkl.com', 'password': 'password',
                               'name_first': 'elevenchars',
                               'name_last': 'ninecharso'})
    assert resp2.status_code == 200

    # use users/all to get all user info
    resp3 = requests.get(config.url + 'users/all/v1', params={'token': token})
    assert resp3.status_code == 200
    get = resp3.json()

    # assert handle strings were sliced correctly and that user2's handle will
    # have a digit at the end
    assert get['users'][0]['handle_str'] == 'abcdefghijklmnopqrst'
    assert get['users'][1]['handle_str'] == 'firstabcdefghijklmno'
    assert get['users'][2]['handle_str'] == 'elevencharsninechars'

def test_create_handle_longer_than_twenty_duplicate():
    """ testing if users/all returns the right handle value when there are two
    users with the same name and their name is longer than 20 characters """
    
    requests.delete(config.url + 'clear/v1')

    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': name_22_chars,
                               'name_last': 'last'})
    assert resp0.status_code == 200
    user1 = resp0.json()
    token = user1['token']

    resp1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': name_22_chars,
                               'name_last': 'last'})
    assert resp1.status_code == 200

    resp2 = requests.get(config.url + 'users/all/v1', params={'token': token})
    assert resp2.status_code == 200
    get = resp2.json()

    # assert handle strings were sliced correctly
    assert get['users'][0]['handle_str'] == 'abcdefghijklmnopqrst'
    assert get['users'][1]['handle_str'] == 'abcdefghijklmnopqrst0'

def test_create_handle_symbols():
    """ testing if channel_details_v1 returns the right handle value when there
    are two users with the same name and their name is longer than 20 characters
    """

    requests.delete(config.url + 'clear/v1')

    # create a user with names including spaces and symbols
    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': '@bcdefgh!j',
                               'name_last': 'klmn opqrst'})
    assert resp0.status_code == 200
    user1 = resp0.json()
    token = user1['token']

    # use users/all to get all user info
    resp1 = requests.get(config.url + 'users/all/v1', params={'token': token})
    assert resp1.status_code == 200
    get = resp1.json()

    # assert that all symbols and spaces aren't included in the handle_str
    assert get['users'][0]['handle_str'] == 'bcdefghjklmnopqrst'

requests.delete(config.url + 'clear/v1')
