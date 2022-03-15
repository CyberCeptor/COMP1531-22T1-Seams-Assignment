"""
Filename: channel_test.py

Author: Yangjun Yue(z5317840), Zefan Cao(z5237177), Xingjian Dong (z5221888)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_details_v1, channel_invite_v1 and
            channel join_v1, channel_messages_v1
"""

import pytest

from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channel import channel_invite_v1, channel_details_v1
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
        channel_invite_v1(id1, 0, id2)

def test_channel_invite_self(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee
    with given information, testing invalid invitee to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid invitee

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    with pytest.raises(InputError):
        channel_invite_v1(id1, chan_id1, id1)

def test_channel_invite_invalid_inviter(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing invalid inviter to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid inviter

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    with pytest.raises(AccessError):
        channel_invite_v1(2, chan_id1, id1)
    with pytest.raises(InputError):
        channel_invite_v1(-2, chan_id1, id1)
    with pytest.raises(InputError):
        channel_invite_v1(True, chan_id1, id1)
    with pytest.raises(InputError):
        channel_invite_v1('3', chan_id1, id1)

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
        channel_invite_v1(id1, chan_id1, 2)
    with pytest.raises(InputError):
        channel_invite_v1(id1, chan_id1, -2)
    with pytest.raises(InputError):
        channel_invite_v1(id1, chan_id1, True)
    with pytest.raises(InputError):
        channel_invite_v1(id1, chan_id1, '3')

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
    id2 = user2['auth_user_id']
    channel_join_v1(id2, chan_id1)
    with pytest.raises(InputError):
        channel_invite_v1(id1, chan_id1, id2)

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
    id1 = user1['auth_user_id']
    chan1 = channels_create_v1(id1, 'namelwky', True)
    chan_id1 = chan1['channel_id']

    user2 = auth_register_v1('xue4@gmail.com', 'xzq19991123', 'Xue', 'zhan')
    id2 = user2['auth_user_id']

    user3 = auth_register_v1('wan3@gmail.com', 'wky191123', 'Wang', 'kaan')
    id3 = user3['auth_user_id']
    with pytest.raises(AccessError):
        channel_invite_v1(id3, chan_id1, id2)

def test_channel_invite_invalid_user_id(clear_and_register_and_create):
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
        channel_join_v1(2, chan_id1)
    with pytest.raises(InputError):
        channel_join_v1(-2, chan_id1)
    with pytest.raises(InputError):
        channel_join_v1(True, chan_id1)
    with pytest.raises(InputError):
        channel_join_v1('3', chan_id1)
    with pytest.raises(InputError):
        channel_join_v1('', chan_id1)

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

def test_channel_details_invalid_user_id(clear_and_register_and_create):
    """
    testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    chan_id1 = clear_and_register_and_create[1]
    # no user input
    with pytest.raises(InputError):
        channel_details_v1('', chan_id1)
    # wrong type user input
    with pytest.raises(InputError):
        channel_details_v1('not int', chan_id1)
    # wrong type user input
    with pytest.raises(InputError):
        channel_details_v1(True, chan_id1)
    # user is not in the channel
    with pytest.raises(AccessError):
        channel_details_v1(2, chan_id1)
    # non exist user input
    with pytest.raises(InputError):
        channel_details_v1(-1, chan_id1)

def test_channel_details_invalid_channel(clear_and_register_and_create):
    """
    testing invalid channel id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    # no channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, '')
    # wrong channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, -1)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, 'not int')
    # non-existant channel
    with pytest.raises(InputError):
        channel_details_v1(id1, 6)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, True)

def test_channel_details_return(clear_and_register_and_create):
    """
    testing if channel_details_v1 returns right values

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    result = channel_details_v1(id1, chan_id1)
    assert result == {
        'name': 'channel_name',
        'is_public': True,
        'owner_members': [{
            'u_id': id1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast'
        }],
        'all_members': [{
            'u_id': id1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast'
        }]
    }

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
