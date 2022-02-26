
import pytest
from src.auth import auth_register_v1
from src.channels import channels_create_v1
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

# A Dictionary for auth_register_v1 input
generic_user = {
    "email": "abc@def.com",
    "password": "password",
    "first_name": "first",
    "last_name": "last",
}




### auth['auth_user_id'] is accessing the item in the Dictionary of User.
### is_public is True and False, so need to test for both public and private channels.

# Testing create only works with valid auth_user_id. Access Error
def test_channels_create_valid_auth_id():
    clear_v1()
    with pytest.raises(AccessError):
        assert channels_create_v1('-4', 'test_channel_public', True)
        assert channels_create_v1('-4', 'test_channel_private', False)

# Testing channel name is greater then 1 character, gives no input for name. Input Error
def test_channels_create_too_short():
    clear_v1()
    #return auth_user_id
    auth = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    assert channels_create_v1(auth['auth_user_id'], "", True)
    assert channels_create_v1(auth['auth_user_id'], "", False)

# Testing for channel name longer than 20 characters for both public and private channels. InputError.
def test_channels_create_channel_name_too_long():
    clear_v1()
    auth = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    with pytest.raises(InputError):
        assert channels_create_v1(auth['auth_user_id'], 'MoreThan20CharPublic!', True)
        assert channels_create_v1(auth['auth_user_id'], 'MoreThan20CharPrivate', False)

# Testing that the is_public argument is a boolean. Input Error
def test_channels_create_boolean():
    clear_v1()
    auth = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    with pytest.raises(InputError):
        assert channels_create_v1(auth['auth_user_id'], 'test_channel', 'Not a boolean')

# Source code https://pythonguides.com/python-check-if-the-variable-is-an-integer/
# Testing the return value of channels_create is a valid int for both public and private. 
def test_channels_create_return():
    clear_v1()
    auth = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channel_id_one = channels_create_v1(auth['auth_user_id'], 'test_channel_public', True)
    channel_id_two = channels_create_v1(auth['auth_user_id'], 'test_channel_private', False)
    with pytest.raises(AccessError):
        assert isinstance(channel_id_one['channel_id'], int)
        assert isinstance(channel_id_two['channel_id'], int)



#####################################################
#       Channels List Test Functions                #
#####################################################


def test_channels_list_v1():
    clear_v1()
    channel1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')


# Testing the channels_list_v1 when multiple channels are created and added to it.


