"""
Filename: admin_userpermission_change_test.py

Author: Aleesha, z5371516
Created: 22/03/22 - 27/03/22

Description: pytests for admin/userpermission/change/v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register_two')
def test_admin_userpermission_change_works(clear_register_two):
    """ user1, a global owner, changes the permissions of user2, a normal
    member, so that they also become a global owner """

    token1 = clear_register_two[0]['token']
    id1 = clear_register_two[0]['auth_user_id']

    token2 = clear_register_two[1]['token']
    id2 = clear_register_two[1]['auth_user_id']

    # change user2 to a global owner
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token1, 'u_id': id2,
                                'permission_id': 1})
    assert resp0.status_code == 200

    # user2 can now demote user1 to a normal user
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token2, 'u_id': id1,
                                'permission_id': 2})
    assert resp0.status_code == 200

@pytest.mark.usefixtures('clear_register_two')
def test_admin_userpermission_change_invalid_token(clear_register_two):
    """ tests userpermission/change with invalid token inputs """

    id2 = clear_register_two[1]['auth_user_id']

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

@pytest.mark.usefixtures('clear_register_two')
def test_admin_userpermission_change_invalid_u_id(clear_register_two):
    """ tests userpermission/change with invalid u_id inputs """

    token = clear_register_two[0]['token']

    # input error: negative u_id
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': -1,
                                'permission_id': 1})
    assert resp0.status_code == 400

    # input error: non-existant u_id
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': 44, 'permission_id': 1})
    assert resp1.status_code == 400

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

@pytest.mark.usefixtures('clear_register_two')
def test_admin_userpermission_change_invalid_perm_id(clear_register_two):
    """ tests userpermission/change with invalid permission_id inputs """

    token = clear_register_two[0]['token']
    id2 = clear_register_two[1]['auth_user_id']

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

@pytest.mark.usefixtures('clear_register_two')
def test_admin_userpermission_change_not_global_owner(clear_register_two):
    """ a user who is not a global owner attempts to change the permissions of
    another user"""

    token2 = clear_register_two[1]['token']

    # create a third user
    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'ghi@jkl.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user3 = resp0.json()
    id3 = user3['auth_user_id']

    # user 2 who is not a global owner tries to make user3 a global owner
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token2, 'u_id': id3,
                                'permission_id': 1})
    assert resp1.status_code == 403

@pytest.mark.usefixtures('clear_register_two')
def test_admin_userpermission_change_one_global_owner(clear_register_two):
    """ there is only one global owner and they are trying to demote themselves
    to a normal user """

    token = clear_register_two[0]['token']
    id = clear_register_two[0]['auth_user_id']

    # demoting own permissions but there is only one global owner
    resp = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id,
                                'permission_id': 2})
    assert resp.status_code == 400

@pytest.mark.usefixtures('clear_register_two')
def admin_userpermission_change_unchanged_perms(clear_register_two):
    """ a global owner is trying to change the permission ids of themselves and
    another user to permission they already have """

    token = clear_register_two[0]['token']
    id1 = clear_register_two[0]['auth_user_id']
    id2 = clear_register_two[1]['auth_user_id']

    # already a global owner
    resp0 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id1,
                                'permission_id': 1})
    assert resp0.status_code == 400

    # already a member
    resp1 = requests.post(config.url + 'admin/userpermission/change/v1',
                          json={'token': token, 'u_id': id2,
                                'permission_id': 2})
    assert resp1.status_code == 400

requests.delete(config.url + 'clear/v1')
