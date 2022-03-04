"""
Filename: channel_test.py

Author: Yangjun Yue(z5317840), Zefan Cao(z5237177)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_details_v1, channel_invite_v1 and channel join_v1
"""

import pytest
from src.channel import channel_details_v1
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.channels import channels_create_v1
from src.channel import channel_invite_v1
from src.channel import channel_join_v1

#### Test Chanel_invite    Zefan Cao(Van) z5237177
#
#
#
# Inputerror:Test the function has an invalid channel_id
def test_invite_wrong_channel():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_invite_v1(1, 0, 2)

# Inputerror:Test the function has an invalid invitee.
def test_invite_wrong_invitee():
    clear_v1()
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_invite_v1(1, 1, invitee_info['auth_user_id'])

# Inputerror:Test the function has an invalid inviter.
def test_invite_wrong_inviter():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    with pytest.raises(AccessError):
        channel_invite_v1(1, 1, 2)

# Inputerror:Test the invitee is already in channel
def test_channel_invite_user_already_joined():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    channels_create_v1(inviter_info['auth_user_id'], 'namewkychannel', True)
    channel_join_v1(invitee_info['auth_user_id'], 1)
    with pytest.raises(InputError):
        channel_invite_v1(invitee_info['auth_user_id'],1, 1)

# Accesserror: Test the inviter is not in the channel
def test_channel_invite_not_in_channel():
    clear_v1()
    truowner_info = auth_register_v1('limingzhe@gmail.com', 'lmz19991123', 'Li', 'mingzhe')
    createchannel =channels_create_v1(truowner_info['auth_user_id'], 'namechatnnelwky', True)  
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    with pytest.raises(AccessError):
        channel_invite_v1(inviter_info['auth_user_id'], createchannel['channel_id'], invitee_info['auth_user_id'])

######## Test channel_join_v1 Zefan Cao z5237177
#
#
#
# InputError:Channel is an invalid channel
def test_join_invalid_channel():
    clear_v1()
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_join_v1(1, 0)

# Inputerror: user is already in channel
def test_join_already_exist():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    channels_create_v1(1, 'validchannelname', True)
    with pytest.raises(InputError):
        channel_join_v1(1, 1)

# AccessError: channel is valid that is private and the user is not a global owner
def test_join_channel_is_private():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    newchannel = channels_create_v1(inviter_info['auth_user_id'], 'validchannelname', False) # it is a private channel
    with pytest.raises(AccessError):
        channel_join_v1(invitee_info['auth_user_id'], newchannel['channel_id'])


########
#
#
@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'channel_name', True)

# testing input user id is valid
def test_channel_details_invalid_user_type(clear_and_register_and_create):
    """ testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A """

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

# channel id does not refer to a valid channel
def test_channel_details_invalid_channel(clear_and_register_and_create):
    """ testing invalid channel id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A """

    # pylint: disable=unused-argument

    # no channel id input
    with pytest.raises(InputError):
        channel_details_v1(1,'')
    # wrong channel id input
    with pytest.raises(InputError):
        channel_details_v1(1,-1)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(1,'not int')

# Testing valid type for channel_details_v1
def test_channel_details_return(clear_and_register_and_create):
    """ testing if channel_details_v1 returns right values

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A """

    # pylint: disable=unused-argument

    result = channel_details_v1(1, 1)
    assert result == {
        'name': 'channel_name',
        'is_public': True,
        'owner_members': [1],
        'all_members': [1],
    }

clear_v1()
