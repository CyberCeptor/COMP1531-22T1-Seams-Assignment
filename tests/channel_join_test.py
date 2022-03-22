"""
Filename: channel_test.py

Author: Zefan Cao(z5237177)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel join_v1
"""
import pytest
import requests
from src import config

@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'abc@def.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    data = resp.json()
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': data['token'], 'name': 'channel_name',
                            'is_public': True})

    data1 = chan.json()
    return [data['token'], data1['channel_id'], data['auth_user_id']]

def test_channel_join_successfully(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee, a inviter
    with given information, create a channel with user id, add user with token

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    chan1_id = clear_and_register_and_create[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data1 = resp1.json()
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': data1['token'],
                        'channel_id': chan1_id})
    assert add.status_code == 200

def test_channel_join_invalid_token(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing invalid token to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid inviter

    Return Value: N/A
    """
    chan_id1 = clear_and_register_and_create[1]
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': 2, 'channel_id': chan_id1})
    assert add.status_code == 400
    
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': -2, 'channel_id': chan_id1})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': True, 'channel_id': chan_id1})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': '3', 'channel_id': chan_id1})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': '', 'channel_id': chan_id1})
    assert add.status_code == 403

def test_channel_join_invalid_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee with
    given information, testing an invalid channel to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invalid channel

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': 5})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': True})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': -5})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': 0})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': '6'})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': ''})
    assert add.status_code == 400

def test_channel_join_user_already_in_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee with
    given information, testing a invitee is alredy in channel to raise input
    error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for a invitee(already in channel)

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    add = requests.post(config.url + 'channel/join/v2',
                        json={'token': id1, 'channel_id': chan_id1})
    assert add.status_code == 400

def test_channel_join_private_channel():
    """
    clears any data stored in data_store and registers a invitee, a inviter
    with given information, create a channel with user id, testing the channel
    is private to raise access error

    Arguments: N/A

    Exceptions:
        AccessError - Raised for a channel is private

    Return Value: N/A
    """
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
    assert add.status_code == 403

requests.delete(config.url + 'clear/v1')