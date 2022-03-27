"""
Filename: dm_remove_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: pytest for dm_remove
"""
import pytest
import requests
from src import config

@pytest.mark.usefixtures('clear_register')
def test_dm_remove_invalid_token(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm remove successfully

    Arguments: clear_and_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    id1 = clear_register['auth_user_id']
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    token2 = data1['token']
    
    create = requests.post(config.url + 'dm/create/v1', 
                json={'token': token2, 'u_ids': [id1]})
    data2 = create.json()
    dm_id = data2['dm_id']
    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': 500, 'dm_id': dm_id})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': -500, 'dm_id': dm_id})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': '', 'dm_id': dm_id})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': 's', 'dm_id': dm_id})
    assert remove.status_code == 403

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': False, 'dm_id': dm_id})
    assert remove.status_code == 400

def test_dm_remove_valid(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm remove successfully

    Arguments: clear_and_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register['token']
    id1 = clear_register['auth_user_id']
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
    token2 = data1['token']
    
    create = requests.post(config.url + 'dm/create/v1', 
                json={'token': token2, 'u_ids': [id1]})
    data2 = create.json()
    dm_id = data2['dm_id']
    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token2, 'dm_id': dm_id})
    assert remove.status_code == 200

    create = requests.post(config.url + 'dm/create/v1', 
                json={'token': token1, 'u_ids': [id2]})
    data2 = create.json()
    dm_id = data2['dm_id']
    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token1, 'dm_id': dm_id})
    assert remove.status_code == 200

    create = requests.post(config.url + 'dm/create/v1', 
                json={'token': token1, 'u_ids': [id2, id1]})
    assert create.status_code == 400

def test_dm_remove_invalid_u_id(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raise inputerror by invalid u_id

    Arguments: clear_and_register(fixture)

    Exceptions: InputError - raised by invalid u_id

    Return Value: N/A
    """
    id1 = clear_register['auth_user_id']
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    token2 = data1['token']

    requests.post(config.url + 'dm/create/v1', 
                json={'token': token2, 'u_ids': [id1]})
    
    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token2, 'dm_id': ''})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token2, 'dm_id': 'dfg'})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token2, 'dm_id': True})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token2, 'dm_id': 900})
    assert remove.status_code == 400

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token2, 'dm_id': -900})
    assert remove.status_code == 400

def test_dm_remove_not_creator(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raise accesserror by not a creator

    Arguments: clear_and_register(fixture)

    Exceptions: AccessError - raised by not a creator

    Return Value: N/A
    """
    token1 = clear_register['token']
    id1 = clear_register['auth_user_id']
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    token2 = data1['token']
    create = requests.post(config.url + 'dm/create/v1', 
                json={'token': token2, 'u_ids': [id1]})
    data2 = create.json()
    dm_id = data2['dm_id']
    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token1, 'dm_id': dm_id})
    assert remove.status_code == 403

def test_dm_remove_not_in_dm(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raise accesserror by not in dm

    Arguments: clear_and_register(fixture)

    Exceptions: AccessError - raised by not in dm

    Return Value: N/A
    """
    token1 = clear_register['token']
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2]})
    data2 = create.json()
    dm_id = data2['dm_id']
    requests.post(config.url + 'dm/leave/v1', 
                json={'token': token1, 'dm_id': dm_id})
    remove = requests.delete(config.url + 'dm/remove/v1', 
                json={'token': token1, 'dm_id': dm_id})
    assert remove.status_code == 403
requests.delete(config.url + 'clear/v1')