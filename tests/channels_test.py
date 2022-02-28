import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
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


def test_channels_list_v1():
    clear_v1()
    channel1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    clear_v1()


# Testing the channels_list_v1 when multiple channels are created and added to it.



