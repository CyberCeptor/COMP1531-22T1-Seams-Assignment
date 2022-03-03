from unicodedata import name
import pytest

from src.auth import auth_register_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError

user1 = {
    'email': 'abd.def@com',
    'pw': 'password',
    'first': 'first',
    'last': 'last',
    'handle_str': 'firstlast'
}

channel1 = {
    'name': 'channel_name',
    'is_public': True
}

users = [user1]

@pytest.fixture
def user_create():
    for user in users:
        result = auth_register_v1(
            user["email"], user["pw"], 
            user["first"], user["last"]
        )
        user1['id'] = result['auth_user_id']

@pytest.fixture
def channel_create():
    clear_v1()
    result = channels_create_v1(
        user1['id'], channel1['name'], 
        channel1['is_public']
    )
    channel1['channel_id'] = result['channel_id']

# Testing valid type for channel_details_v1
def test_channels_details_return():
    result = channel_details_v1(user1['id'],channel1['channel_id'])
    user = {
        "u_id": user1['id'],
        "email": user1['email'],
        "name_first": user1['first'],
        "name_last": user1['last'],
        "handle_str": user1['handle_str'],
    }
    assert result == {
        "name": channel1['name'],
        "is_public": channel1['is_public'],
        "owner_members": user,
        "all_members": user,
    }
clear_v1()


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



