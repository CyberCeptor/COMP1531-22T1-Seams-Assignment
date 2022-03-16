"""
Filename: channel_test.py

Author: Aleesha, z5371516
Created: 09/03/2022

Description: pytests for handle generation from auth_register_v1
"""

import pytest

from src.auth import auth_register_v1

from src.other import clear_v1

from src.channel import channel_details_v1, channel_join_v1

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

def test_create_handle_duplicate(clear_and_register_and_create):
    """
    testing if channel_details_v1 returns thr right handle values when there are
    two users with the same first and last name

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]

    user2 = auth_register_v1('def@ghi.com', 'password', 'first', 'last')
    id2 = user2['auth_user_id']
    channel_join_v1(id2, chan_id1)

    result = channel_details_v1(id1, chan_id1)
    assert result['all_members'][0]['handle_str'] == 'firstlast'
    assert result['all_members'][1]['handle_str'] == 'firstlast0'

def test_create_handle_longer_than_twenty():
    """
    testing if channel_details_v1 returns the right handle values when there are
    users with a name longer than 20 characters

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    name22 = 'abcdefghijklmnopqrstuv'

    user1 = auth_register_v1('abc@def.com', 'password', name22, 'last')
    id1 = user1['auth_user_id']

    chan1 = channels_create_v1(id1, 'channel_name', True)
    chan_id1 = chan1['channel_id']

    user2 = auth_register_v1('def@ghi.com', 'password', 'first', name22)
    id2 = user2['auth_user_id']
    channel_join_v1(id2, chan_id1)

    result = channel_details_v1(id1, chan_id1)
    assert result['all_members'][0]['handle_str'] == 'abcdefghijklmnopqrst'
    assert result['all_members'][1]['handle_str'] == 'firstabcdefghijklmno'

def test_create_handle_longer_than_twenty_duplicate():
    """
    testing if channel_details_v1 returns the right handle value when there are
    two users with the same name and their name is longer than 20 characters

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    name22 = 'abcdefghijklmnopqrstuv'

    user1 = auth_register_v1('abc@def.com', 'password', name22, 'last')
    id1 = user1['auth_user_id']

    chan1 = channels_create_v1(id1, 'channel_name', True)
    chan_id1 = chan1['channel_id']

    user2 = auth_register_v1('def@ghi.com', 'password', name22, 'last')
    id2 = user2['auth_user_id']
    channel_join_v1(id2, chan_id1)

    result = channel_details_v1(id1, chan_id1)
    assert result['all_members'][0]['handle_str'] == 'abcdefghijklmnopqrst'
    assert result['all_members'][1]['handle_str'] == 'abcdefghijklmnopqrst0'

def test_create_handle_symbols():
    """
    testing if channel_details_v1 returns the right handle value when there are
    two users with the same name and their name is longer than 20 characters

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v1('a@d.com', 'password', '@bcdefgh!j', 'klmn opqrst')
    id1 = user1['auth_user_id']

    chan1 = channels_create_v1(id1, 'channel_name', True)
    chan_id1 = chan1['channel_id']

    result = channel_details_v1(id1, chan_id1)
    assert result['all_members'][0]['handle_str'] == 'bcdefghjklmnopqrst'

clear_v1()
