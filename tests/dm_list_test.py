"""
Filename: dm_list_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description:http pytest for dm_list
"""
import pytest
import requests
from src import config

@pytest.mark.usefixtures('clear_register_createdm')
def test_dm_list_valid(clear_register_createdm):
    """
    clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token

    Arguments: clear_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register_createdm[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data2 = resp1.json()
    id3 = data2['auth_user_id']
    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': token1})
    assert list1.status_code == 200
    
    requests.post(config.url + 'dm/create/v1', 
                json={'token': token1, 'u_ids': [id3]})
    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': token1})
    assert list1.status_code == 200

@pytest.mark.usefixtures('clear_register_two')
def test_dm_list_invalid_token(clear_register_two):
    """
    clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token

    Arguments: clear_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register_two[0]['token']
    id2 = clear_register_two[1]['auth_user_id']
    requests.post(config.url + 'dm/create/v1', 
                json={'token': token1, 'u_ids': [id2]})
    
    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': 500})
    assert list1.status_code == 400

    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': -500})
    assert list1.status_code == 400

    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': True})
    assert list1.status_code == 400

    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': ''})
    assert list1.status_code == 400

    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': 'ads'})
    assert list1.status_code == 403

requests.delete(config.url + 'clear/v1')