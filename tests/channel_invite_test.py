"""
Filename: channel_test.py

Author: Zefan Cao(z5237177)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_invite_v1
"""

import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_invite_v2, channel_join_v2
from src.channels import channels_create_v1

@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    clear_v1()
    user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    chan1 = channels_create_v1(user1['token'], 'channel_name', True)
    return [user1['token'], chan1['channel_id'], user1['auth_user_id']]

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
    user2 = auth_register_v1('xue2@gmail.com', 'xzq191123', 'Xue', 'zhiqian')
    id1 = clear_and_register_and_create[0]
    id2 = user2['auth_user_id']
    with pytest.raises(InputError):
        channel_invite_v2(id1, 0, id2)

def test_channel_invite_self(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing inviter invite himself

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for inviter invite himself

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    id2 = clear_and_register_and_create[2]
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, id2)

def test_channel_invite_invalid_token(clear_and_register_and_create):
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
    with pytest.raises(AccessError):
        channel_invite_v2(2, chan_id1, id1)
    with pytest.raises(InputError):
        channel_invite_v2(-2, chan_id1, id1)
    with pytest.raises(InputError):
        channel_invite_v2(True, chan_id1, id1)
    with pytest.raises(InputError):
        channel_invite_v2('3', chan_id1, id1)

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
    with pytest.raises(AccessError):
        channel_invite_v2(id1, chan_id1, 2)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, -2)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, True)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, '3')

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

    user2 = auth_register_v1('xue2@gmail.com', 'xzq191123', 'Xue', 'zhan')
    id2 = user2['token']
    id3 = user2['auth_user_id']
    channel_join_v2(id2, chan_id1)
    with pytest.raises(InputError):
        channel_invite_v2(id1, chan_id1, id3)

def test_channel_invite_inviter_not_in_channel():
    """
    clears any data stored in data_store and registers a inviter, a invitee,
    the owner of channel with the given information,
    create a channel with user id, and then use the inviter(is not in channel)
    to add the invitee to raise a access error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        AccessError: Raised for a invter(not in channel) add the invitee

    Return Value: N/A
    """

    clear_v1()
    user1 = auth_register_v1('li@gmail.com', 'lmz191123', 'Li', 'minge')
    id1 = user1['token']
    chan1 = channels_create_v1(id1, 'namelwky', True)
    chan_id1 = chan1['channel_id']

    user2 = auth_register_v1('xue4@gmail.com', 'xzq19991123', 'Xue', 'zhan')
    id2 = user2['auth_user_id']

    user3 = auth_register_v1('wan3@gmail.com', 'wky191123', 'Wang', 'kaan')
    id3 = user3['token']
    with pytest.raises(AccessError):
        channel_invite_v2(id3, chan_id1, id2)

def test_channel_join_invalid_token(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing invalid inviter to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid inviter

    Return Value: N/A
    """
    chan_id1 = clear_and_register_and_create[1]
    with pytest.raises(AccessError):
        channel_join_v2(2, chan_id1)
    with pytest.raises(InputError):
        channel_join_v2(-2, chan_id1)
    with pytest.raises(InputError):
        channel_join_v2(True, chan_id1)
    with pytest.raises(InputError):
        channel_join_v2('3', chan_id1)
    with pytest.raises(InputError):
        channel_join_v2('', chan_id1)

clear_v1()
