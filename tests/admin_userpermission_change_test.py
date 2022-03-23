"""
Filename: admin_userpermission_change_test.py

Author: Aleesha, z5371516
Created: 22/03/22

Description: pytests for
    - changing the permission of a specified user
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

    Return Value: N/A """

    # clear_v1()
    # auth_register_v1('abc@def.com', 'password', 'first', 'last')
    requests.delete(config.url + 'clear/v1')

    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    return resp.json()

def test_admin_userpermission_change_works(clear_and_register):
    token = clear_and_register['token']

    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 1})
    assert resp1.status_code == 200

def test_admin_userpermission_change_invalid_token(clear_and_register):
    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    # input error: int is passed in as token
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': 1, 'u_id': id2,
                                'permission_id': 1})
    assert resp1.status_code == 400

    # input error: normal string is passed in as token
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': 'not a valid jwt token str',
                                'u_id': id2, 'permission_id': 1})
    assert resp2.status_code == 403

    # input error: bool is passed in as token
    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': True, 'u_id': id2,
                                'permission_id': 1})
    assert resp3.status_code == 400

    expired_unsaved = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2l\
                        vbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3OT\
                        c3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'

    # access error: expired, unsaved token
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': expired_unsaved, 'u_id': id2,
                                'permission_id': 1})
    assert resp4.status_code == 403

    unsaved = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI\
                6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR\
                -m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'

    # access error: unexpired, unsaved token
    resp5 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': unsaved, 'u_id': id2,
                                'permission_id': 1})
    assert resp5.status_code == 403

    # access error: empty str is passed in as token
    resp6 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': '', 'u_id': id2, 'permission_id': 1})
    assert resp6.status_code == 400

def test_admin_userpermission_change_user_logged_out(clear_and_register):
    token = clear_and_register['token']

    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    # log user1 out and try to change user2's perm id using user1's token
    resp1 = requests.post(config.url + 'auth/logout/v1', json={'token': token})
    assert resp1.status_code == 200

    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 1})
    assert resp2.status_code == 403

def test_admin_userpermission_change_invalid_u_id(clear_and_register):
    token = clear_and_register['token']

    # input error: negative u_id
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': -1,
                                'permission_id': 1})
    assert resp1.status_code == 400

    # input error: non-existant u_id
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': 44, 'permission_id': 1})
    assert resp2.status_code == 403

    # input error: bool
    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': True,
                                'permission_id': 1})
    assert resp3.status_code == 400

    resp4 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': False,
                                'permission_id': 1})
    assert resp4.status_code == 400

    # input error: str is passed in as u_id
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': 'str',
                                'permission_id': 1})
    assert resp4.status_code == 400

    # input error: empty str is passed in as u_id
    resp5 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': '',
                                'permission_id': 1})
    assert resp5.status_code == 400 

def test_admin_userpermission_change_invalid_permission_id(clear_and_register):
    token = clear_and_register['token']

    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    # input error: invalid permission id number
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 4})
    assert resp1.status_code == 400

    # input error: bool is passed in as permission id
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': True})
    assert resp2.status_code == 400

    # input error: str is passed in as permission id
    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 'global'})
    assert resp3.status_code == 400

    # input error: empty str is passed in as permission id
    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': ''})
    assert resp3.status_code == 400

def test_admin_userpermission_change_not_global_owner(clear_and_register):
    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    token2 = user2['token']

    resp1 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'ghi@jkl.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 200
    user3 = resp0.json()
    id3 = user3['auth_user_id']

    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token2, 'u_id': id3,
                                'permission_id': 1})
    assert resp2.status_code == 403

def test_admin_userpermission_change_one_global_owner(clear_and_register):
    token = clear_and_register['token']
    id = clear_and_register['auth_user_id']

    # input error: demoting own permissions but there is only one global owner
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id,
                                'permission_id': 2})
    assert resp0.status_code == 400

def admin_userpermission_change_unchanged_perms(clear_and_register):
    token = clear_and_register['token']
    id1 = clear_and_register['auth_user_id']

    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    # input error: already a global owner
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id1,
                                'permission_id': 1})
    assert resp1.status_code == 400

    # input error: already a member
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 2})
    assert resp2.status_code == 400

requests.delete(config.url + 'clear/v1')
