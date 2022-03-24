"""
Filename: admin_userpermission_change_test.py

Author: Aleesha, z5371516
Created: 22/03/22

Description: pytests for changing the permission of a specified user
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register_two_users():
    """ clears any data stored in data_store and registers a user with the
    given information """

    requests.delete(config.url + 'clear/v1')

    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user1 = resp0.json()

    resp1 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 200
    user2 = resp1.json()

    return [user1, user2]

def test_admin_userpermission_change_works(clear_and_register):
    """ user1, a global owner, changes the permissions of user2, a normal
    member, so that they also become a global owner """

    token = clear_and_register[0]['token']
    id2 = clear_and_register[1]['auth_user_id']

    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 1})
    assert resp0.status_code == 200

def test_admin_userpermission_change_invalid_token(clear_and_register):
    """ invalid tokens passed in """

    id2 = clear_and_register[1]['auth_user_id']

    # input error: int is passed in as token
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': 1, 'u_id': id2,
                                'permission_id': 1})
    assert resp0.status_code == 400

    # input error: normal string is passed in as token
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': 'not a valid jwt token str',
                                'u_id': id2, 'permission_id': 1})
    assert resp1.status_code == 403

    # input error: bool is passed in as token
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': True, 'u_id': id2,
                                'permission_id': 1})
    assert resp2.status_code == 400

    # access error: expired, unsaved token
    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': expired_token, 'u_id': id2,
                                'permission_id': 1})
    assert resp3.status_code == 403

    # access error: unexpired, unsaved token
    resp4 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': unsaved_token, 'u_id': id2,
                                'permission_id': 1})
    assert resp4.status_code == 403

    # input error: empty str is passed in as token
    resp5 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': '', 'u_id': id2, 'permission_id': 1})
    assert resp5.status_code == 400

def test_admin_userpermission_change_user_logged_out(clear_and_register):
    """ a global owner who has logged out uses their now unsaved token to change
    the permissions of another user """

    token = clear_and_register[0]['token']
    id2 = clear_and_register[1]['auth_user_id']

    resp0 = requests.post(config.url + 'auth/logout/v1', json={'token': token})
    assert resp0.status_code == 200

    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 1})
    assert resp1.status_code == 403

def test_admin_userpermission_change_invalid_u_id(clear_and_register):
    """ invalid u_ids passed in """

    token = clear_and_register[0]['token']

    # input error: negative u_id
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': -1,
                                'permission_id': 1})
    assert resp0.status_code == 400

    # input error: non-existant u_id
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': 44, 'permission_id': 1})
    assert resp1.status_code == 403

    # input error: bool
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': True,
                                'permission_id': 1})
    assert resp2.status_code == 400

    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': False,
                                'permission_id': 1})
    assert resp3.status_code == 400

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
    """ invalid permission ids passed in """

    token = clear_and_register[0]['token']
    id2 = clear_and_register[1]['auth_user_id']

    # input error: invalid permission id number
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 4})
    assert resp0.status_code == 400

    # input error: bool is passed in as permission id
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': True})
    assert resp1.status_code == 400

    # input error: str is passed in as permission id
    resp2 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 'global'})
    assert resp2.status_code == 400

    # input error: empty str is passed in as permission id
    resp3 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': ''})
    assert resp3.status_code == 400

def test_admin_userpermission_change_not_global_owner(clear_and_register):
    """ a user who is not a global owner attempts to change the permissions of
    another user"""

    token2 = clear_and_register[1]['token']

    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'ghi@jkl.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user3 = resp0.json()
    id3 = user3['auth_user_id']

    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token2, 'u_id': id3,
                                'permission_id': 1})
    assert resp1.status_code == 403

def test_admin_userpermission_change_one_global_owner(clear_and_register):
    """ there is only one global owner and they are trying to demote themselves
    to a normal user """

    token = clear_and_register[0]['token']
    id = clear_and_register[0]['auth_user_id']

    # input error: demoting own permissions but there is only one global owner
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id,
                                'permission_id': 2})
    assert resp0.status_code == 400

def admin_userpermission_change_unchanged_perms(clear_and_register):
    """ a global owner is trying to change the permission ids of themselves and
    another user to permission they already have """

    token = clear_and_register[0]['token']
    id1 = clear_and_register[0]['auth_user_id']
    id2 = clear_and_register[1]['auth_user_id']

    # input error: already a global owner
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id1,
                                'permission_id': 1})
    assert resp0.status_code == 400

    # input error: already a member
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 2})
    assert resp1.status_code == 400

requests.delete(config.url + 'clear/v1')
