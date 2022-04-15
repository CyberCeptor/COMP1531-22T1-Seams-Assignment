"""
Filename: dm_remove_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: pytest for dm_remove
"""

import pytest

import requests

from src import config

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_remove_invalid_token(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, run dm remove successfully """

    dm_id = clear_register_two_createdm[2]
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

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_remove_valid(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, run dm remove successfully """

    token1 = clear_register_two_createdm[0]['token']
    id1 = clear_register_two_createdm[0]['auth_user_id']
    id2 = clear_register_two_createdm[1]['auth_user_id']
    token2 = clear_register_two_createdm[1]['token']
    
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

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_remove_invalid_u_id(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raise inputerror by invalid u_id """

    token2 = clear_register_two_createdm[2]

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

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_remove_not_creator(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raise accesserror by not a creator """

    token1 = clear_register_two_createdm[1]['token']
    dm_id = clear_register_two_createdm[2]

    remove = requests.delete(config.url + 'dm/remove/v1', 
                        json={'token': token1, 'dm_id': dm_id})
    assert remove.status_code == 403

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_remove_not_in_dm(clear_register_two_createdm):
    """ clears any data stored in data_store and registers a user with the
    given information, raise accesserror by not in dm """

    token1 = clear_register_two_createdm[1]['token']
    dm_id = clear_register_two_createdm[2]
    requests.post(config.url + 'dm/leave/v1', 
                json={'token': token1, 'dm_id': dm_id})
    remove = requests.delete(config.url + 'dm/remove/v1', 
                json={'token': token1, 'dm_id': dm_id})
    assert remove.status_code == 403

requests.delete(config.url + 'clear/v1')
