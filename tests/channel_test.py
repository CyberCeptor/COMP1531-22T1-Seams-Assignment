from unicodedata import name
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

# Testing valid type for channel_details_v1
def test_channels_details_return():
    result = channel_details_v1(1, 1)
    assert result == {
        "name": 'channel_name',
        "is_public": True,
        "owner_members": 1,
        "all_members": 1,
    }
clear_v1()


# testing input user id is valid
def test_valid_auth_user_id():
    # no user input
    with pytest.raises(InputError):
        channel_details_v1('', 1)
    clear_v1()
    # non exist user inpt
    with pytest.raises(AccessError):
        channel_details_v1(-1, 1)
    clear_v1()
    # wrong type user input
    with pytest.raises(InputError):
        channel_details_v1('not int',1)
    clear_v1()

# channel id does not refer to a valid channel
def test_channel_detail_invalid_channel():
    # no channel id inpujt
    with pytest.raises(InputError):
        channel_details_v1(1,'')
    clear_v1()
    # wrong channel id input
    with pytest.raises(InputError):
        channel_details_v1(1,-1)
    clear_v1()
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(1,'not int')
    clear_v1()

# channel id valid but user is not a member of
def test_channel_detail_invalid_user():
    with pytest.raises(AccessError):
        channel_details_v1(2, 1)
    clear_v1()



