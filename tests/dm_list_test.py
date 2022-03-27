"""
Filename: dm_list_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description:http pytest for dm_list
"""
import pytest
import requests
from src import config

@pytest.fixture(name='clear_register')
def fixture_clear_register():
    """
    clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: data['token']
                  data['auth_user_id']
    """

    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'wky@gmail.com', 'password': '547832',
                                'name_first': 'wang', 'name_last': 'kaiyan'})
    data = resp.json()
    return [data['token'], data['auth_user_id']]

def test_dm_list_valid(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token

    Arguments: clear_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    data2 = resp2.json()
    id2 = data1['auth_user_id']
    id3 = data2['auth_user_id']
    requests.post(config.url + 'dm/create/v1', 
                json={'token': token1, 'u_ids': [id2]})
    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': token1})
    assert list1.status_code == 200
    
    requests.post(config.url + 'dm/create/v1', 
                json={'token': token1, 'u_ids': [id3]})
    list1 = requests.get(config.url + 'dm/list/v1',
                params={'token': token1})
    assert list1.status_code == 200

def test_dm_list_invalid_token(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token

    Arguments: clear_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
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