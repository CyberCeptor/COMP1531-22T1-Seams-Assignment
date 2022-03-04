import pytest

from src.auth import auth_register_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

@pytest.fixture
def clear_and_register_and_create():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'channel_name', True)

# testing input user id is valid
def test_channel_details_invalid_user_type(clear_and_register_and_create):
    # no user input
    with pytest.raises(InputError):
        channel_details_v1('', 1)
    # wrong type user input
    with pytest.raises(InputError):
        channel_details_v1('not int',1)

def test_channel_details_invalid_user(clear_and_register_and_create):
    # user does not exist
    with pytest.raises(AccessError):
        channel_details_v1(2, 1)
    # non exist user input
    with pytest.raises(AccessError):
        channel_details_v1(-1, 1)

# channel id does not refer to a valid channel
def test_channel_details_invalid_channel(clear_and_register_and_create):
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
    result = channel_details_v1(1, 1)
    assert result == {
        'name': 'channel_name',
        'is_public': True,
        'owner_members': [1],
        'all_members': [1],
    }

clear_v1()
