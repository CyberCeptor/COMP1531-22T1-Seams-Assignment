"""
Filename: dm_leave_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http pytest for dm_leave
"""
import pytest
import requests
from src import config

@pytest.mark.usefixtures('clear_register_createdm')
def test_dm_leave_invalid_token(clear_register_createdm):
    """
    clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id

    Arguments: clear_register(fixture)

    Exceptions: InputErroe - raised by invalid token

    Return Value: N/A
    """
    dm_id = clear_register_createdm[1]
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

@pytest.mark.usefixtures('clear_register_createdm')
def test_dm_leave_valid(clear_register_createdm):
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm details successful

    Arguments: clear_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    token1 = clear_register_createdm[0]
    dm_id = clear_register_createdm[1]
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': dm_id})
    assert leave.status_code == 200

@pytest.mark.usefixtures('clear_register_two')
def test_dm_leave_invalid_dm_id(clear_register_two):
    """
    clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id

    Arguments: clear_register(fixture)

    Exceptions: InputErroe - raised by invalid dm_id

    Return Value: N/A
    """
    token1 = clear_register_two[0]['token']
    id1 = clear_register_two[0]['auth_user_id']
    id2 = clear_register_two[1]['auth_user_id']
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

@pytest.mark.usefixtures('clear_register_createdm')
def test_dm_leave_notin_dm(clear_register_createdm):
    """
    clears any data stored in data_store and registers a user with the
    given information, raise a access error by the auth not in dm

    Arguments: clear_register(fixture)

    Exceptions: AccessError - raised by auth not in dm

    Return Value: N/A
    """
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data2 = resp1.json()
    token3 = data2['token']
    dm_id = clear_register_createdm[1]
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token3, 'dm_id': dm_id})
    assert leave.status_code == 403

requests.delete(config.url + 'clear/v1')
