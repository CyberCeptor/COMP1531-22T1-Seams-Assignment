"""
Filename: channels_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_list_v1
"""

import pytest

from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channels import channels_create_v1, channels_list_v1

def test_channels_list_valid_id():
    """
    Creates a 2 channels:
        -   tests if given a non-existant
        user_id it raises an accesserror
        -   tests for non-int input (bool, string)
    Arguments:  N/A

    Exceptions:
        AccessError  - raised for non-user_id
        InputError  - for non int input

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    id1 = user1['auth_user_id']
    channels_create_v1(id1, 'test_channel', True)
    channels_create_v1(id1, 'test_channel', False)
    with pytest.raises(AccessError):
        channels_list_v1(2)
    with pytest.raises(InputError):
        channels_list_v1(-2)
    with pytest.raises(InputError):
        channels_list_v1(True)
    with pytest.raises(InputError):
        channels_list_v1('String')
    with pytest.raises(InputError):
        channels_list_v1('')

def test_channels_list_id_check():
    """
    Create channel, and test a non-valid id.

    Arguments: N/A

    Exceptions:
        AccessError -   for the non valid id case below

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    id1 = user1['auth_user_id']
    channels_create_v1(id1, 'test_channel_public', True)
    channels_create_v1(id1, 'test_channel_private', False)
    # auth_id 1 has created two channels, there is no user 4444 to create the
    # channels list.
    with pytest.raises(AccessError):
        channels_list_v1(44444) # give incorrect auth_id.

def test_channels_list_v1():
    """
    Test that the channels list is functionally with multiple channels being
    created. This also tests for public and private channels.
    Also tests that channel_list only returns the channel that the id is in.

    Arguments:  N/A

    Exceptions: N/A

    Return Value:   N/A
    """

    clear_v1()
    user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    id1 = user1['auth_user_id']
    chan1 = channels_create_v1(id1, 'test_channel_public1', True)
    chan2 = channels_create_v1(id1, 'test_channel_public2', True)
    chan3 = channels_create_v1(id1, 'test_channel_priv1', False)
    chan4 = channels_create_v1(id1, 'test_channel_priv2', False)

    # adding some random channels from another user to makes sure its not
    # returning all channels, even those which the user isnt in.
    user2 = auth_register_v1('def@abc.com', 'password', 'first', 'last')
    id2 = user2['auth_user_id']
    channels_create_v1(id2, 'test2_channel_pub', True)
    channels_create_v1(id2, 'test2_channel_priv', False)
    # returns a Dict containing 'channel_id' and 'name' of all channels the user
    # is in.
    channels_list = channels_list_v1(id1)
    channels_list_v1(id2)

    # check the first four channels in the dict, check that the channel_id
    # matches what was created.
    assert channels_list['channels'][0]['channel_id'] == chan1['channel_id']
    assert channels_list['channels'][1]['channel_id'] == chan2['channel_id']
    assert channels_list['channels'][2]['channel_id'] == chan3['channel_id']
    assert channels_list['channels'][3]['channel_id'] == chan4['channel_id']

    # Testing to make sure that only 4 channels have been created for that user.
    assert len(channels_list['channels']) == 4

clear_v1()