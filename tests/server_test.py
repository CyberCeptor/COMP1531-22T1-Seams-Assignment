import pytest

import requests

from src import config

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    # clear_v1()
    # auth_register_v1('abc@def.com', 'password', 'first', 'last')
    requests.delete(config.url + 'clear/v1')

    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    return resp.json()

def test_logout_works(clear_and_register):
    token = clear_and_register['token']

    resp1 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': token})
    assert resp1.status_code == 200

def test_logout_invalid_token(clear_and_register):
    # input error: int is passed in as token
    resp0 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': 1})
    assert resp0.status_code == 400

    # access error: non-jwt token str is passed in as token
    resp1 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': 'not a valid jwt token str'})
    assert resp1.status_code == 403

    # input error: bool is passed in as token
    resp2 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': True})
    assert resp2.status_code == 400

def test_users_return():
    requests.delete(config.url + 'clear/v1')

    resp0 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    user1 = resp0.json()
    id1 = user1['auth_user_id']

    resp1 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'def@ghi.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    user2 = resp1.json()
    id2 = user2['auth_user_id']

    resp = requests.get(config.url + 'users/all/v1')
    data = resp.json()
    print(data)
    assert len(data) == 2
    assert data == [{
        'u_id': id1,
        'email': 'abc@def.com',
        'name_first': 'first',
        'name_last': 'last',
        'handle_str': 'firstlast'
        }, {
        'u_id': id2,
        'email': 'def@ghi.com',
        'name_first': 'first',
        'name_last': 'last',
        'handle_str': 'firstlast0'
    }]
