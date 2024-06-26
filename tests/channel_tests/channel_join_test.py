"""
Filename: channel_join_test.py

Author: Zefan Cao(z5237177)
Created: 28/02/2022 - 27/03/2022

Description: pytests for channel join_v1
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK, STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_join_successfully(clear_register_createchannel):
    """ clears any data stored in data_store and registers a invitee, a inviter
    with given information, create a channel with user id, add user with token
    """

    chan1_id = clear_register_createchannel[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data1 = resp1.json()
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': data1['token'],
                        'channel_id': chan1_id})
    assert add.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_join_invalid_token(clear_register_createchannel):
    """ clears any data stored in data_store and registers a inviter
    with given information, testing invalid token to raise input error """

    chan_id1 = clear_register_createchannel[1]
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': 2, 'channel_id': chan_id1})
    assert add.status_code == STATUS_INPUT_ERR
    
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': -2, 'channel_id': chan_id1})
    assert add.status_code == STATUS_INPUT_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': True, 'channel_id': chan_id1})
    assert add.status_code == STATUS_INPUT_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': 'goood', 'channel_id': chan_id1})
    assert add.status_code == STATUS_ACCESS_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': '', 'channel_id': chan_id1})
    assert add.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_join_invalid_channel(clear_register_createchannel):
    """ clears any data stored in data_store and registers a invitee with
    given information, testing an invalid channel to raise input error """

    id1 = clear_register_createchannel[0]['token']
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': 5})
    assert add.status_code == STATUS_INPUT_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': True})
    assert add.status_code == STATUS_INPUT_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': -5})
    assert add.status_code == STATUS_INPUT_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': '6'})
    assert add.status_code == STATUS_INPUT_ERR

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': ''})
    assert add.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_join_user_already_in_channel(clear_register_createchannel):
    """ clears any data stored in data_store and registers a invitee with
    given information, testing a invitee is alredy in channel to raise input """

    id1 = clear_register_createchannel[0]['token']
    chan_id1 = clear_register_createchannel[1]
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': chan_id1})
    assert add.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_join_private_channel():
    """ clears any data stored in data_store and registers a invitee, a inviter
    with given information, create a channel with user id, testing the channel
    is private to raise a access error """

    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'abc@def.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    data = resp.json()
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data1 = resp1.json()
    
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': data['token'], 'name': 'channel_name',
                            'is_public': False})
    data2 = chan.json()
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': data1['token'],
                        'channel_id': data2['channel_id']})
    assert add.status_code == STATUS_ACCESS_ERR

requests.delete(config.url + 'clear/v1')
