"""
Filename: users_all_test.py

Author: Aleesha Bunrith(z5371516)
Created: 21/03/2022 - 27/03/22

Description: pytests for users/all/v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register')
def test_users_all_return(clear_register):
    """ test users/all works using the response """

    token1 = clear_register['token']
    id1 = clear_register['auth_user_id']

    # create a second user
    resp0 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'def@ghi.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    token2 = user2['token']
    id2 = user2['auth_user_id']

    # use user1's token to get the info of all users
    resp1 = requests.get(config.url + 'users/all/v1', params={'token': token1})
    assert resp1.status_code == 200
    get1 = resp1.json()

    # check the response is same as expected
    assert len(get1['users']) == 2
    
    assert id1 in [k['u_id'] for k in get1['users']]
    assert 'abc@def.com' in [k['email'] for k in get1['users']]
    assert 'first' in [k['name_first'] for k in get1['users']]
    assert 'last' in [k['name_last'] for k in get1['users']]
    assert 'firstlast' in [k['handle_str'] for k in get1['users']]

    assert id2 in [k['u_id'] for k in get1['users']]
    assert 'def@ghi.com' in [k['email'] for k in get1['users']]
    assert 'first' in [k['name_first'] for k in get1['users']]
    assert 'last' in [k['name_last'] for k in get1['users']]
    assert 'firstlast0' in [k['handle_str'] for k in get1['users']]

    # use user1's token to get the info of all users, reponse will be the same
    resp2 = requests.get(config.url + 'users/all/v1', params={'token': token2})
    assert resp2.status_code == 200
    get2 = resp2.json()
    assert get1 == get2

@pytest.mark.usefixtures('clear_register')
def test_users_all_invalid_token(clear_register):
    """ test users/all with invalid token input """

    # input error: int is passed in as token
    resp0 = requests.get(config.url + 'users/all/v1', params={'token': 1})
    assert resp0.status_code == 400

    # input error: not jwt token str is passed in as token
    resp1 = requests.get(config.url + 'users/all/v1',
                         params={'token': 'not a valid jwt token str'})
    assert resp1.status_code == 403

    # input error: bool is passed in as token
    resp2 = requests.get(config.url + 'users/all/v1', params={'token': True})
    assert resp2.status_code == 400

    # access error: expired, unsaved token
    resp3 = requests.get(config.url + 'users/all/v1',
                         params={'token': expired_token})
    assert resp3.status_code == 403

    # access error: unexpired, unsaved token
    resp3 = requests.get(config.url + 'users/all/v1', 
                         params={'token': unsaved_token})
    assert resp3.status_code == 403

    # input error: empty str passed in as token 
    resp4 = requests.get(config.url + 'users/all/v1', params={'token': ''})
    assert resp4.status_code == 400

requests.delete(config.url + 'clear/v1')
