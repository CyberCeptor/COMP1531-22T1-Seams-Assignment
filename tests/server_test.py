import pytest

import requests

from src import config

<<<<<<< HEAD
EXPIRED = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
=======
EXPIRED = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSw\
    iaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLV\
        NlGLX_INKVwr8_TVXYEQ'
>>>>>>> master

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

<<<<<<< HEAD
    resp1 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': token})
    assert resp1.status_code == 200
=======
    resp = requests.post(config.url + 'auth/logout/v1',
                         json={'token': token})
    assert resp.status_code == 200
>>>>>>> master

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

    # access error: expired, unsaved token
    resp3 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': EXPIRED})
    assert resp3.status_code == 403

<<<<<<< HEAD
def test_users_return(clear_and_register):
=======
def test_users_all_return(clear_and_register):
>>>>>>> master
    token1 = clear_and_register['token']
    id1 = clear_and_register['auth_user_id']

    resp0 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'def@ghi.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    token2 = user2['token']
    id2 = user2['auth_user_id']

    resp1 = requests.get(config.url + 'users/all/v1', params={'token': token1})
    assert resp1.status_code == 200
    get1 = resp1.json()

    assert len(get1['users']) == 2
    assert get1['users'] == [{
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

    resp2 = requests.get(config.url + 'users/all/v1', params={'token': token2})
    assert resp2.status_code == 200
    get2 = resp2.json()
    assert get1 == get2

<<<<<<< HEAD
def test_users_invalid_token(clear_and_register):
=======
def test_users_all_invalid_token(clear_and_register):
>>>>>>> master
    # input error: int is passed in as token
    resp0 = requests.get(config.url + 'users/all/v1', params={'token': 1})
    assert resp0.status_code == 400

    # input error: int is passed in as token
    resp1 = requests.get(config.url + 'users/all/v1',
                         params={'token': 'not a valid jwt token str'})
    assert resp1.status_code == 403

    # input error: int is passed in as token
    resp2 = requests.get(config.url + 'users/all/v1', params={'token': True})
    assert resp2.status_code == 400

    # access error: expired, unsaved token
    resp3 = requests.get(config.url + 'users/all/v1', params={'token': EXPIRED})
    assert resp3.status_code == 403

<<<<<<< HEAD
=======
# def test_users_all_logged_out_user(clear_and_register):
#     token = clear_and_register['token']

#     resp0 = requests.post(config.url + 'auth/logout/v1', json={'token': token})
#     assert resp0.status_code == 200

#     resp3 = requests.get(config.url + 'users/all/v1', params={'token': token})
#     assert resp3.status_code == 403



>>>>>>> master
requests.delete(config.url + 'clear/v1')
