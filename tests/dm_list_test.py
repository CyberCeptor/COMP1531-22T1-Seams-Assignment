"""
Filename: dm_list_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description:http pytest for dm_list
"""

import pytest

import requests

from src import config

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_list_valid(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token """

    token1 = clear_register_two_createdm[0]['token']
    user3 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data3 = user3.json()
    token3 = data3['token']

    list1 = requests.get(config.url + 'dm/list/v1', params={'token': token1})
    assert list1.status_code == 200
    
    # if user is not in any dm
    list2 = requests.get(config.url + 'dm/list/v1',
                params={'token': token3})
    assert list2.status_code == 200

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_list_invalid_token(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token """
    
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
