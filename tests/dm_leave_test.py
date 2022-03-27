"""
Filename: dm_leave_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http pytest for dm_leave
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

def test_dm_leave_invalid_token(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id

    Arguments: clear_register(fixture)

    Exceptions: InputErroe - raised by invalid token

    Return Value: N/A
    """
    token1 = clear_register[0]
    id1 = clear_register[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2]})
    data2 = create.json()
    dm_id = data2['dm_id']
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': 500, 'dm_id': dm_id})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': -500, 'dm_id': dm_id})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': '', 'dm_id': dm_id})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': 'd', 'dm_id': dm_id})
    assert leave.status_code == 403

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': False, 'dm_id': dm_id})
    assert leave.status_code == 400

def test_dm_leave_valid(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm details successful

    Arguments: clear_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id1 = data1['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1]})
    data2 = create.json()
    dm_id = data2['dm_id']
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': dm_id})
    assert leave.status_code == 200

def test_dm_leave_invalid_dm_id(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id

    Arguments: clear_register(fixture)

    Exceptions: InputErroe - raised by invalid dm_id

    Return Value: N/A
    """
    token1 = clear_register[0]
    id1 = clear_register[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
    requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,id2]})
  
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': ''})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': 900})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': -900})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': 'kli'})
    assert leave.status_code == 400

    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': True})
    assert leave.status_code == 400

def test_dm_leave_notin_dm(clear_register):
    """
    clears any data stored in data_store and registers a user with the
    given information, raise a access error by the auth not in dm

    Arguments: clear_register(fixture)

    Exceptions: AccessError - raised by auth not in dm

    Return Value: N/A
    """
    token1 = clear_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id2 = data1['auth_user_id']
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    data2 = resp2.json()
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2]})
    token3 = data2['token']
    data3 = create.json()
    dm_id = data3['dm_id']
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token3, 'dm_id': dm_id})
    assert leave.status_code == 403

requests.delete(config.url + 'clear/v1')
