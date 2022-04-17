"""
Filename: dm_details_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http pytest for dm_details
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK, STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_details_valid(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, run dm details successful """

    token1 = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': dm_id})
    assert detail.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_details_invalid_token(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, run dm details successful """
    
    dm_id = clear_register_two_createdm[2]
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': 500, 'dm_id': dm_id})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': -500, 'dm_id': dm_id})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': '', 'dm_id': dm_id})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': 'sah', 'dm_id': dm_id})
    assert detail.status_code == STATUS_ACCESS_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': False, 'dm_id': dm_id})
    assert detail.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_dm_details_invalid_dm_id(clear_register_two):
    """  clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id """

    token1 = clear_register_two[0]['token']
    id1 = clear_register_two[0]['auth_user_id']
    id2 = clear_register_two[1]['auth_user_id']
    requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,id2]})
  
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': ''})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': 900})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': -900})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': 'kli'})
    assert detail.status_code == STATUS_INPUT_ERR

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': True})
    assert detail.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_details_auth_notin_dm(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raise a access error by the auth not in dm """

    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data2 = resp1.json()
    token3 = data2['token']
    dm_id = clear_register_two_createdm[2]
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token3, 'dm_id': dm_id})
    assert detail.status_code == STATUS_ACCESS_ERR
    
requests.delete(config.url + 'clear/v1')
