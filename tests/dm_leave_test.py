"""
Filename: dm_leave_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http pytest for dm_leave
"""

import pytest

import requests

from src import config

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_leave_invalid_token(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id """

    dm_id = clear_register_two_createdm[2]
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

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_leave_valid(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, run dm details successful"""

    token1 = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token1, 'dm_id': dm_id})
    assert leave.status_code == 200

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_leave_invalid_dm_id(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id """

    token1 = clear_register_two_createdm[0]['token']
  
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

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_leave_not_in_dm(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raise a access error by the auth not in dm """
    
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data2 = resp1.json()
    token3 = data2['token']
    dm_id = clear_register_two_createdm[2]
    leave = requests.post(config.url + 'dm/leave/v1', 
                        json={'token': token3, 'dm_id': dm_id})
    assert leave.status_code == 403

requests.delete(config.url + 'clear/v1')
