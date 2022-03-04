"""
Filename: channels_test.py

Author: Jenson Morgan(z5360181),Yangjun Yue(5317840)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_create_v1, channel_list_v1 and channel_listall_v1
"""

import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

#####################################################
#                                                   #
#          Channels Create Test Functions           #
#                                                   #
#####################################################
'''
Parameters: 
    {auth_user_id,  (int)
    name,           (string)
    is_public}      (Boolean, True/False)

Return Type:
    {channel_id}    (int)
'''

### auth['auth_user_id'] is accessing the item in the Dictionary of User.
### is_public is True and False, so need to test for both public and private channels.
@pytest.fixture
def clear_and_register():
    """
    clears any data stored in data_stored and registers a user with the 
    given information
    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')

# Testing create only works with valid auth_user_id. Access Error
def test_channels_create_valid_auth_id(clear_and_register):
    """
    Registers a valid user, and them
    attempts to create 4 channels with unregistered user_id's, 
    both public and private channels.

    Arguments: clear_and_register

    Exceptions: 
        AccessError - Raised for all tests below

    Return Value: N/A
    """
    with pytest.raises(AccessError):
        channels_create_v1(2, 'test_channel_public', True)
    with pytest.raises(AccessError):
        channels_create_v1(2, 'test_channel_private', False)
    with pytest.raises(AccessError):
        channels_create_v1(-2, 'test_channel_public2', True)
    with pytest.raises(AccessError):
        channels_create_v1(-2, 'test_channel_privat2', False)


def test_channels_create_too_short(clear_and_register):
    """
    Create a channel with no channel name given.
        Tests both public and private channels.

    Arguments: clear_and_register

    Exceptions: 
        InputError  - Raised for all cases below

    Return Value:   N/A
    """
    with pytest.raises(InputError):
        channels_create_v1(1, "", True)
    with pytest.raises(InputError):
        channels_create_v1(1, "", False)


def test_channels_create_invalid_name(clear_and_register):
    """
    Creates a public/private channel with names > 20 characters

    Arguments:  clear_and_register

    Exceptions:
        InputError  -   Raised for all tests below

    Return Value:   N/A
    """
    with pytest.raises(InputError):
        channels_create_v1(1, 'MoreThan20CharPublic!', True)
    with pytest.raises(InputError):
        channels_create_v1(1, 'MoreThan20CharPrivate', False)


def test_channels_create_boolean(clear_and_register):
    """
    Creates a channel with a string as the is_public argument, 
        which should be a boolean.

    Arguments:  clear_and_register

    Exceptions:
        InputError - Raised for the case
    
    Return Value:   N/A
    """
    with pytest.raises(InputError):
        channels_create_v1(1, 'test_channel', 'Not a boolean')


def test_channels_duplicate_name(clear_and_register):
    """
    Creates a channel with an existing channel_name
        Both public and private

    Arguments:  clear_and_register

    Exceptions:
        InputError  -   Raised for all test cases below
    """
    channels_create_v1(1, 'test_channel_public', True)
    with pytest.raises(InputError):  
        channels_create_v1(1, 'test_channel_public', True)

    channels_create_v1(1, 'test_channel_private', False)
    with pytest.raises(InputError):  
        channels_create_v1(1, 'test_channel_private', False)


# Testing the return value of channels_create is a valid int for both public and private. 
def test_channels_create_return(clear_and_register):
    """
    Creates two channels (public and private) and asserts that the
    data returned is correct (1 and 2) as the first 2 channels created.

    Arguments:  clear_and_register

    Exceptions: N/A

    Return Value: N/A
    """
    channel_id_one = channels_create_v1(1, 'test_channel_public', True)
    channel_id_two = channels_create_v1(1, 'test_channel_private', False)
    assert channel_id_one['channel_id'] == 1
    assert channel_id_two['channel_id'] == 2

#####################################################
#                                                   #
#           Channels List Test Functions            #
#                                                   #
#####################################################


"""Check that the given valid exists."""
def test_channels_list_valid_id():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'test_channel', True)
    channels_create_v1(1, 'test_channel', False)
    with pytest.raises(AccessError):
        channels_list_v1(2)
    with pytest.raises(InputError):
        channels_list_v1(True)
    with pytest.raises(InputError):
        channels_list_v1('String')
    


"""check that the given id is in a channel. For both public/private channels created"""
def test_channels_list_id_check():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'test_channel_public', True)
    channels_create_v1(1, 'test_channel_private', False)
    # auth_id 1 has created two channels, there is no user 4444 to create the channels list.
    with pytest.raises(AccessError):
        channels_list_v1(44444) # give incorrect auth_id.

    
"""Test that the channels list is functionally with multiple channels being created.
This also tests for public and private channels.
Also tests that channel_list only returns the channel that the id is in."""
def test_channels_list_v1():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    chan1 = channels_create_v1(1, 'test_channel_public1', True)
    chan2 = channels_create_v1(1, 'test_channel_public2', True)
    chan3 = channels_create_v1(1, 'test_channel_priv1', False)
    chan4 = channels_create_v1(1, 'test_channel_priv2', False)

    # adding some random channels from another user to makes sure its not returning all channels,
    # even those which the user isnt in.
    auth_register_v1('def@abc.com', 'password', 'first', 'last')
    channels_create_v1(2, 'test2_channel_pub', True)
    channels_create_v1(2, 'test2_channel_priv', False)
    
    channels_list = channels_list_v1(1) #returns a Dict containing 'channel_id' and 'name' of all channels the user is in.
    channels_list2 = channels_list_v1(2)

    # check the first four channels in the dict, check that the channel_id matches what was created.
    assert channels_list['channels'][0]['channel_id'] == chan1['channel_id']
    assert channels_list['channels'][1]['channel_id'] == chan2['channel_id']
    assert channels_list['channels'][2]['channel_id'] == chan3['channel_id']
    assert channels_list['channels'][3]['channel_id'] == chan4['channel_id']

    # Testing to make sure that only 4 channels have been created for that user.
    assert len(channels_list['channels']) == 4

    clear_v1()



#####################################################
#                                                   #
#          Channels Listall Test Functions           #
#                                                   #
#####################################################
@pytest.fixture
def clear_and_register_and_create():
    """ 
    Clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A 
    """

    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'channel_name', True)

# testing input user id is valid
def test_valid_auth_user_id(clear_and_register_and_create):
    """ 
    Testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - non existing user id

    Return Value: N/A 
    """

    with pytest.raises(AccessError):
        channels_listall_v1(-1)
    with pytest.raises(AccessError):
        channels_listall_v1(2)

# testing if return values are the right type
def test_channels_listall_v1_return(clear_and_register_and_create):
    """ testing if listall returns right type of value

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/S

    Return Value: N/A 
    """

    result = channels_listall_v1(1)
    assert result['channels'][0] == {
        'channel_id': 1,
        'name': 'channel_name',
    }

clear_v1()
