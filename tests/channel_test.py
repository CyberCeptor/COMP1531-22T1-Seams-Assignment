import pytest

from src.auth import auth_register_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

@pytest.fixture
def clear_and_register():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')

@pytest.fixture
def channel_create():
    clear_v1()
    channels_create_v1('1','channel_name','True')

# testing input user id is valid
def test_valid_auth_user_id():
    # no user input
    with pytest.raises(InputError):
        channel_details_v1('','1')
    clear_v1()
    # non exist user inpt
    with pytest.raises(InputError):
        channel_details_v1('-1','1')
    clear_v1()
    # wrong type user input
    with pytest.raises(InputError):
        channel_details_v1('not int','1')
    clear_v1()

# channel id does not refer to a valid channel
def test_channel_detail_invalid_channel():
    # no channel id inpujt
    with pytest.raises(InputError):
        channel_details_v1('1','')
    clear_v1()
    # wrong channel id input
    with pytest.raises(InputError):
        channel_details_v1('1','-1')
    clear_v1()
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1('1','not int')
    clear_v1()

# channel id valid but user is not a member of
def test_channel_detail_invalid_channel():
    with pytest.raises(InputError):
        channel_details_v1('2','')
    clear_v1()

# Testing valid type for channel_details_v1
def test_channels_create_return(clear_and_register):
    channel_details = channel_details_v1('1','1')
    assert channel_details['name'] == 'channel_name'
    assert channel_details['is_public'] == True
    assert channel_details['owner_members'] == '1'
    assert channel_details['all_members'] == '1'
clear_v1()

