"""
Filename: channel_test.py

Author: Zefan Cao(z5237177)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_invite_v1
"""

from lib2to3.pgen2 import token
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

def test_channel_invite_invalid_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee,
    a inviter with given information, testing invalid channel to raise input
    error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid channel

    Return Value: N/A
    """
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data = resp1.json()
    token = clear_and_register_and_create[0]
    id2 = data['auth_user_id']
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': 44,
                                'u_id': id2})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': False,
                                'u_id': id2})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': -34,
                                'u_id': id2})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': '',
                                'u_id': id2})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': '5',
                                'u_id': id2})
    assert add.status_code == 400

def test_channel_invite_self(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing inviter invite himself

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for inviter invite himself

    Return Value: N/A
    """
    token = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    id = clear_and_register_and_create[2]
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': chan_id1,
                                'u_id': id})
    assert add.status_code == 400

def test_channel_invite_invalid_inviter(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee
    with given information, testing invalid token to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid token

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[2]
    chan_id1 = clear_and_register_and_create[1]
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': -2, 'channel_id': chan_id1,
                                'u_id': id1})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': 2, 'channel_id': chan_id1,
                                'u_id': id1})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': True, 'channel_id': chan_id1,
                                'u_id': id1})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': 'goood', 'channel_id': chan_id1,
                                'u_id': id1})
    assert add.status_code == 403

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': '', 'channel_id': chan_id1,
                                'u_id': id1})
    assert add.status_code == 400

def test_channel_invite_invalid_invitee(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing invalid invitee to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid inviter

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': -2})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': 2})
    assert add.status_code == 403

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': True})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': '3'})
    assert add.status_code == 400
'''
    with pytest.raises(AccessError):
        channel_invite_v2(id1, chan_id1, 2)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, -2)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, True)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, '3')
    '''

def test_channel_invite_invitee_already_joined(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee, a inviter,
    a truowner withi given info, testing a invitee is alredy in channel to raise
    input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for a invitee(already in channel)

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data = resp1.json()
    requests.post(config.url + 'channel/join/v2',
                json={'token': data['token'], 'channel_id': chan_id1})   
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': data['auth_user_id']})
    assert add.status_code == 400

def test_channel_invite_inviter_not_in_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter, a invitee,
    the owner of channel with the given information,
    create a channel with user id, and then use the inviter(is not in channel)
    to add the invitee to raise a access error

    Arguments: clear_and_register_and_create(fixture)

    Exceptions:
        AccessError: Raised for a invter(not in channel) add the invitee

    Return Value: N/A
    """
    chan1_id = clear_and_register_and_create[1]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data2 = resp1.json()
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'wan3@gmail.com', 'password': 'wky19112',
                                'name_first': 'Wang', 'name_last':'kaiyan'})
    data3 = resp2.json()
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': data3['token'],
                                'channel_id': chan1_id,
                                'u_id': data2['auth_user_id']})
    assert add.status_code == 403

requests.delete(config.url + 'clear/v1')
