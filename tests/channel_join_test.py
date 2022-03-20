"""
Filename: channel_test.py

Author: Zefan Cao(z5237177)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel join_v1
"""

import pytest

from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channel import channel_join_v1

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
    chan1 = channels_create_v1(1, 'channel_name', True)
    return [user1['auth_user_id'], chan1['channel_id']]

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
    with pytest.raises(InputError):
        channel_join_v1(id1, 5)
    with pytest.raises(InputError):
        channel_join_v1(id1, True)
    with pytest.raises(InputError):
        channel_join_v1(id1, -5)
    with pytest.raises(InputError):
        channel_join_v1(id1, '6')
    with pytest.raises(InputError):
        channel_join_v1(id1, '')

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
    with pytest.raises(InputError):
        channel_join_v1(chan_id1, id1)

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
    clear_v1()
    user1 = auth_register_v1('wangk@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    id1 = user1['auth_user_id']
    user2 = auth_register_v1('xuezh@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    id2 = user2['auth_user_id']
    chan1 = channels_create_v1(id1, 'validchannelname', False)
    chan_id1 = chan1['channel_id']
    with pytest.raises(AccessError):
        channel_join_v1(id2, chan_id1)

clear_v1()
