import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError



# Assumption that valid login from auth_register.

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
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')

# Testing create only works with valid auth_user_id. Access Error
def test_channels_create_valid_auth_id():
    with pytest.raises(AccessError):
        channels_create_v1(2, 'test_channel_public', True)
    with pytest.raises(AccessError):
        channels_create_v1(2, 'test_channel_private', False)
    with pytest.raises(AccessError):
        channels_create_v1(-2, 'test_channel_public2', True)
    with pytest.raises(AccessError):
        channels_create_v1(-2, 'test_channel_private2', False)

# Testing channel name is greater then 1 character, gives no input for name. Input Error
def test_channels_create_too_short():
    with pytest.raises(InputError):
        channels_create_v1(1, "", True)
    with pytest.raises(InputError):
        channels_create_v1(1, "", False)

# Testing for channel name longer than 20 characters for both public and private channels. InputError.
def test_channels_create_invalid_name():
    with pytest.raises(InputError):
        channels_create_v1(1, 'MoreThan20CharPublic!', True)
    with pytest.raises(InputError):
        channels_create_v1(1, 'MoreThan20CharPrivate', False)

# Testing that the is_public argument is a boolean. Input Error
def test_channels_create_boolean():
    with pytest.raises(InputError):
        channels_create_v1(1, 'test_channel', 'Not a boolean')

# Testing duplicate channels names created with the same is_public.
def test_channels_duplicate_name(clear_and_register):
    channels_create_v1(1, 'test_channel_public3', True)
    with pytest.raises(InputError):  
        channels_create_v1(1, 'test_channel_public3', True)

    channels_create_v1(1, 'test_channel_priv4', False)
    with pytest.raises(InputError):  
        channels_create_v1(1, 'test_channel_priv4', False)


# Testing the return value of channels_create is a valid int for both public and private. 
def test_channels_create_return(clear_and_register):
    channel_id_one = channels_create_v1(1, 'test_channel_public', True)
    channel_id_two = channels_create_v1(1, 'test_channel_private', False)
    assert channel_id_one['channel_id'] == 1
    assert channel_id_two['channel_id'] == 2
    clear_v1()

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
    


"""testing when the channel id is incorrect. For both public/private channels created"""
def test_channels_list_id_check():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'test_channel_public', True)
    channels_create_v1(1, 'test_channel_private', False)
    with pytest.raises(AccessError):
        channels_list_v1(44444) # give incorrect channel_id, should not exist.


"""Test that if the user is not in the channel, channels_list_v1 returns nothing.
There is no channel created, so the user cannot be in any channel."""
def test_channels_list_not_in_channel():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    with pytest.raises(AccessError):
        channels_list_v1(1)
    
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



