"""
Filename: dm_details_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http pytest for dm_details
"""
import pytest
import requests
from src import config

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
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

def test_dm_details_valid(clear_and_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm details successful

    Arguments: clear_and_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_and_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id1 = data1['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1]})
    data2 = create.json()
    dm_id = data2['dm_id']
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': dm_id})
    assert detail.status_code == 200

def test_dm_details_invalid_dm_id(clear_and_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id

    Arguments: clear_and_register(fixture)

    Exceptions: InputErroe - raised by invalid dm_id

    Return Value: N/A
    """
    token1 = clear_and_register[0]
    id1 = clear_and_register[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
    requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,id2]})
  
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': ''})
    assert detail.status_code == 400

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': 900})
    assert detail.status_code == 400

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': -900})
    assert detail.status_code == 400

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': 'kli'})
    assert detail.status_code == 400

    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token1, 'dm_id': True})
    assert detail.status_code == 400

def tetest_dm_details_auth_notin_dm(clear_and_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raise a access error by the auth not in dm

    Arguments: clear_and_register(fixture)

    Exceptions: AccessError - raised by auth not in dm

    Return Value: N/A
    """
    token1 = clear_and_register[0]
    id1 = clear_and_register[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    token2 = data1['token']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1]})
    data2 = create.json()
    dm_id = data2['dm_id']
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token2, 'dm_id': dm_id})
    assert detail.status_code == 403
requests.delete(config.url + 'clear/v1')