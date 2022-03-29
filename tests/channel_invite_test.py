"""
Filename: channel_invite_test.py

Author: Zefan Cao(z5237177)
Created: 28/02/2022 - 27/03/2022

Description: pytests for channel_invite_v1
"""

import pytest

import requests

from src import config

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_invalid_channel(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a invitee,
    a inviter with given information, testing invalid channel to raise input
    error

    Arguments: clear_register_createchannel (fixture)

    Exceptions:
        InputError - Raised for an invlaid channel

    Return Value: N/A
    """

    token = clear_register_createchannel[0]['token']
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    data = resp1.json()
    
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

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_self(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing inviter invite himself

    Arguments: clear_register_createchannel (fixture)

    Exceptions:
        InputError - Raised for inviter invite himself

    Return Value: N/A
    """
    token = clear_register_createchannel[0]['token']
    chan_id1 = clear_register_createchannel[1]
    id = clear_register_createchannel[0]['token']
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': token, 'channel_id': chan_id1,
                                'u_id': id})
    assert add.status_code == 400

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_invalid_inviter(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a invitee
    with given information, testing invalid token to raise input error

    Arguments: clear_register_createchannel (fixture)

    Exceptions:
        InputError - Raised for an invlaid token

    Return Value: N/A
    """
    id1 = clear_register_createchannel[0]['auth_user_id']
    chan_id1 = clear_register_createchannel[1]
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


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_invalid_invitee(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing invalid invitee to raise input error

    Arguments: clear_register_createchannel (fixture)

    Exceptions:
        InputError - Raised for an invlaid inviter

    Return Value: N/A
    """
    id1 = clear_register_createchannel[0]['token']
    chan_id1 = clear_register_createchannel[1]
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': -2})
    assert add.status_code == 400

    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': 2})
    assert add.status_code == 400

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

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_invitee_already_joined(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a invitee, a inviter,
    a truowner withi given info, testing a invitee is alredy in channel to raise
    input error

    Arguments: clear_register_createchannel (fixture)

    Exceptions:
        InputError - Raised for a invitee(already in channel)

    Return Value: N/A
    """
    id1 = clear_register_createchannel[0]['token']
    chan_id1 = clear_register_createchannel[1]
    # create user 2
    create_user2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    user2 = create_user2.json()

    # user 2 joins channel 1
    requests.post(config.url + 'channel/join/v2',
                json={'token': user2['token'], 'channel_id': chan_id1})  
    # user 1 invites user 2
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': user2['auth_user_id']})
    assert add.status_code == 400


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_inviter_not_in_channel(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a inviter, a invitee,
    the owner of channel with the given information,
    create a channel with user id, and then use the inviter(is not in channel)
    to add the invitee to raise a access error

    Arguments: clear_register_createchannel(fixture)

    Exceptions:
        AccessError: Raised for a invter(not in channel) add the invitee

    Return Value: N/A
    """
    chan1_id = clear_register_createchannel[1]
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


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_invite_success(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a invitee, a inviter,
    a truowner withi given info, testing a invitee is alredy in channel to raise
    input error

    Arguments: clear_register_createchannel (fixture)

    Exceptions:
        InputError - Raised for a invitee(already in channel)

    Return Value: N/A
    """
    id1 = clear_register_createchannel[0]['token']
    chan_id1 = clear_register_createchannel[1]
    # create user 2
    create_user2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    user2 = create_user2.json()

    # user 1 invites user 2
    add = requests.post(config.url + 'channel/invite/v2', 
                        json={'token': id1, 'channel_id': chan_id1,
                                'u_id': user2['auth_user_id']})
    assert add.status_code == 200
