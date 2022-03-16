"""
Filename: channel_test.py

Author: Xingjian Dong (z5221888)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_messages_v1
"""

import pytest

from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channel import channel_details_v1
from src.channel import channel_join_v1, channel_messages_v1

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

def test_channel_messages_invalid_channel(clear_and_register_and_create):
    """
    testing invalid channel id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: InputError - Raised for all test cases listed below

    Return Value: N/A
    """

    id1 = clear_and_register_and_create[0]
    # no channel id input
    with pytest.raises(InputError):
        channel_messages_v1(id1, '', 0)
    # wrong channel id input
    with pytest.raises(InputError):
        channel_messages_v1(id1, -1, 0)
    # wrong channel id input
    with pytest.raises(InputError):
        channel_messages_v1(id1, 5, 0)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_messages_v1(id1, 'not int', 0)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_messages_v1(id1, True, 0)

def test_channel_messages_invalid_user_id(clear_and_register_and_create):
    """
    testing unauthorised user to raise access error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: AccessError - Raised for all test cases listed below

    Return Value: N/A
    """

    chan_id1 = clear_and_register_and_create[1]

    # no user input
    with pytest.raises(InputError):
        channel_messages_v1('', chan_id1, 0)
    # wrong type user input
    with pytest.raises(InputError):
        channel_messages_v1('not int', chan_id1, 0)
    # wrong type user input
    with pytest.raises(InputError):
        channel_messages_v1(True, chan_id1, 0)
    # user is not in the channel
    with pytest.raises(AccessError):
        channel_messages_v1(2, chan_id1, 0)
    # non exist user input
    with pytest.raises(InputError):
        channel_messages_v1(-1, chan_id1, 0)

clear_v1()
