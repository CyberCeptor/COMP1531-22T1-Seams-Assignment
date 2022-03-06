"""
Filename: channel_test.py

Author: Yangjun Yue(z5317840), Zefan Cao(z5237177)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_details_v1, channel_invite_v1 and
            channel join_v1
"""

import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_invite_v1, channel_details_v1, channel_join_v1
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
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'channel_name', True)

#####################################################
#                                                   #
#          Channels Invite Test Functions           #
#                                                   #
#####################################################
#written by zefan cao z5237177

# Inputerror:Test the function has an invalid channel
def test_channel_invite_invalid_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee, a inviter
    with given information, testing invalid channel to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid channel

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    auth_register_v1('xue2@gmail.com', 'xzq191123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_invite_v1(1, 0, 2)

# Inputerror:Test the function has an invalid invitee.
def test_channel_invite_self(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee
    with given information, testing invalid invitee to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid invitee

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    with pytest.raises(InputError):
        channel_invite_v1(1, 1, 1)

# Inputerror:Test the function has an invalid inviter.
def test_channel_invite_invalid_invitee(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a inviter
    with given information, testing invalid inviter to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invlaid inviter

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    with pytest.raises(AccessError):
        channel_invite_v1(1, 1, 2)

# Inputerror:Test the invitee is already in channel
def test_channel_invite_invitee_already_joined(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee, a inviter,
    a truowner withi given info, testing a invitee is alredy in channel
    to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for a invitee(already in channel)

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    invitee_info = auth_register_v1('xue@gmail.com', 'xzq19123', 'Xue', 'zhan')
    channel_join_v1(invitee_info['auth_user_id'], 1)
    with pytest.raises(InputError):
        channel_invite_v1(1, 1, 2)

# Accesserror: Test the inviter is not in the channel
def test_channel_invite_inviter_not_in_channel(clear_and_register_and_create):
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
    # pylint: disable=unused-argument
    clear_v1()
    inviter_info = auth_register_v1('li@gmail.com', 'lmz191123', 'Li', 'minge')
    createchannel = channels_create_v1(inviter_info['auth_user_id'],
                    'namelwky', True)
    invitee_info = auth_register_v1('xue@gmail.com', 'xzq191123', 'Xue', 'zan')
    inviter_info = auth_register_v1('wan3@gmail.com', 'wky1923', 'Wang', 'kaan')
    with pytest.raises(AccessError):
        channel_invite_v1(inviter_info['auth_user_id'],
        createchannel['channel_id'], invitee_info['auth_user_id'])

#####################################################
#                                                   #
#          Channels Join Test Functions             #
#                                                   #
#####################################################
#written by zefan cao z5237177

# Inputerror: channel is invalid
def test_channel_join_invalid_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee with
    given information, testing an invalid channel to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for an invalid channel

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    with pytest.raises(InputError):
        channel_join_v1(1, 0)

# Inputerror: user is already in channel
def test_channel_join_user_already_in_channel(clear_and_register_and_create):
    """
    clears any data stored in data_store and registers a invitee with
    given information, testing a invitee is alredy in channel to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for a invitee(already in channel)

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    with pytest.raises(InputError):
        channel_join_v1(1, 1)

# AccessError: channel is valid that is private and the user is not a global owner
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
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    newchannel = channels_create_v1(inviter_info['auth_user_id'], 'validchannelname', False)
    with pytest.raises(AccessError):
        channel_join_v1(invitee_info['auth_user_id'], newchannel['channel_id'])

#####################################################
#                                                   #
#          Channels Details Test Functions          #
#                                                   #
#####################################################
def test_channel_details_invalid_user_type(clear_and_register_and_create):
    """
    testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    # no user input
    with pytest.raises(InputError):
        channel_details_v1('', 1)
    # wrong type user input
    with pytest.raises(InputError):
        channel_details_v1('not int',1)
    # user is not in the channel
    with pytest.raises(AccessError):
        channel_details_v1(2, 1)
    # non exist user input
    with pytest.raises(AccessError):
        channel_details_v1(-1, 1)

def test_channel_details_invalid_channel(clear_and_register_and_create):
    """
    testing invalid channel id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    # no channel id input
    with pytest.raises(InputError):
        channel_details_v1(1, '')
    # wrong channel id input
    with pytest.raises(InputError):
        channel_details_v1(1, -1)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(1, 'not int')

def test_channel_details_return(clear_and_register_and_create):
    """
    testing if channel_details_v1 returns right values

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    result = channel_details_v1(1, 1)
    assert result == {
        'name': 'channel_name',
        'is_public': True,
        'owner_members': [1],
        'all_members': [1],
    }

clear_v1()
