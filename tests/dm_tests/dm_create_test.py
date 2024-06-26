"""
Filename: dm_create_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: pytest for dm_create
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK, STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_create_valid(clear_register_two_createdm):
    """ clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids """

    token1 = clear_register_two_createdm[0]['token']
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    data2 = resp2.json()
    id2 = clear_register_two_createdm[1]['auth_user_id']
    id3 = data2['auth_user_id']

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2,id3]})
    assert create.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register')
def test_dm_create_token_invalid(clear_register):
    """ clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids """

    id1 = clear_register['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': 500, 'u_ids': [id1]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': -500, 'u_ids': [id1]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': '', 'u_ids': [id1]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': True, 'u_ids': [id1]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': 'sbfg', 'u_ids': [id1]})
    assert create.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_dm_create_invalid_uid(clear_register_two):
    """ clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids """

    token1 = clear_register_two[0]['token']
    id1 = clear_register_two[1]['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,-500]})
    assert create.status_code == STATUS_INPUT_ERR
    
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,500]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,False]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,'s']})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,'']})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1',
                        json={'token': token1, 'u_ids': ['j',id1]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1',
                        json={'token': token1, 'u_ids': id1})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1',
                        json={'token': token1, 'u_ids': True})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1',
                        json={'token': token1, 'u_ids': ''})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1',
                        json={'token': token1, 'u_ids': 'str'})
    assert create.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_dm_create_duplicate_uid(clear_register_two):
    """ clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids """

    token1 = clear_register_two[0]['token']
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    data2 = resp2.json()
    id2 = clear_register_two[1]['auth_user_id']
    id3 = data2['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2,id2]})
    assert create.status_code == STATUS_INPUT_ERR

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id3,id3]})
    assert create.status_code == STATUS_INPUT_ERR

def test_dm_create_creator_in_uids(clear_register):
    """ clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids  """

    token1 = clear_register['token']
    id1 = clear_register['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1]})
    assert create.status_code == STATUS_INPUT_ERR

requests.delete(config.url + 'clear/v1')