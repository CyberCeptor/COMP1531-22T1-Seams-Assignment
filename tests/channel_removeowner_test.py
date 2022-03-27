import pytest
import requests

from src import config
from src.global_vars import expired_token, unsaved_token

@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    Clears.
    Creates 2 users, and a channel with both members as owners
    """
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user1_data = user1.json()
    user1_token = user1_data['token']
    user1_id = user1_data['auth_user_id']

    user2 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc2@def.com', 'password': 'password2',
                               'name_first': 'first2', 'name_last': 'last2'})
    user2_data = user2.json()
    user2_id = user2_data['auth_user_id']
    user2_token = user2_data['token']

    channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': user1_token, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = channel.json()
    channel_id = channel_data['channel_id']

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user2 to be an owner, with user1's token as they are owner_member
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 200

    return [user1_id, user1_token, user2_id, user2_token, channel_id]


def test_channel_removeowner_working(clear_and_register_and_create):
    """
    2 users both owner_members of a channel,
    user2 removes themselves as owner,
    user1 adds them back as an owner,
    assert the channel information is correct.
    """
    user1_id = clear_and_register_and_create[0]
    user1_token = clear_and_register_and_create[1]
    user2_id = clear_and_register_and_create[2]
    user2_token = clear_and_register_and_create[3]
    channel_id = clear_and_register_and_create[4]

    
    # user2 removing themselves as a owner_member
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 200

    # add user2 to be an owner, with user1's token as they are owner_member
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 200

    # user2 being removed as owner_member with user1's token
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 200

    # check the data in the channel is correct
    channels_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1_token, 'channel_id': channel_id})
    channels_json = channels_details.json()

    assert len(channels_json['owner_members']) == 1
    assert channels_json['owner_members'] == [{
        'u_id': user1_id,
        'email': 'abc@def.com',
        'name_first': 'first',
        'name_last': 'last',
        'handle_str': 'firstlast'
    }]

def test_channel_removeowner_permission_id(clear_and_register_and_create):
    """
    2 users both owner_members of a channel,
    user2 removes themselves as owner,
    user3 is created and joins the channel and made owner_member,
    (needed as the last owner_member cant remove themselves as owner_member)
    user2 tries to remove user1 as owner,
    user2 becomes a global owner of the channel,
    (a global owner can add/remove owners as long as they are also a member,
    they dont have to be owner, just all_member)
    user2 then removes user1 as owner
    """
    user1_id = clear_and_register_and_create[0]
    user1_token = clear_and_register_and_create[1]
    user2_id = clear_and_register_and_create[2]
    user2_token = clear_and_register_and_create[3]
    channel_id = clear_and_register_and_create[4]

    # remove user2 as owner_member
    addowner = requests.post(config.url + 'channel/removeowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 200

    # create user3 and set them as an owner_member of the channel
    user3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc3@def.com', 'password': 'password3',
                               'name_first': 'first3', 'name_last': 'last3'})
    user3_data = user3.json()
    user3_token = user3_data['token']
    user3_id = user3_data['auth_user_id']

    # add user3 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user3_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user3 to be an owner, with user1's token as they are owner_member
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert addowner.status_code == 200

    # user2 cant remove user1 as they are not a global member or an owner_member
    removeowner = requests.post(config.url + 'channel/removeowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': user1_id})
    assert removeowner.status_code == 403

    # setting user2 to global owner
    global_perm = requests.post(config.url + 'admin/userpermission/change/v1', 
                        json={'token': user1_token, 'u_id': user2_id, 'permission_id': 1})
    assert global_perm.status_code == 200

    # user2 can now remove user3 as they are not a owner_member, but are a global owner
    addowner = requests.post(config.url + 'channel/removeowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': user1_id})
    assert addowner.status_code == 200


def test_channel_removeowner_not_an_owner(clear_and_register_and_create):
    """
    2 owner_members of channel,
    user2 removed as owner,
    assert user 2 is still an all_member of the channel,
    user1 tries to remove user2 as an owner again,
    InputError
    """
    user1_token = clear_and_register_and_create[1]
    user2_id = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[4]

    # user2 being removed as an owner
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 200

    # Test that user2 is still an all_members member.
    channels_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1_token, 'channel_id': channel_id})
    channels_json = channels_details.json()

    # Check that the all_members dict is untouched. And user2 is removed from owner_members
    assert len(channels_json['owner_members']) == 1
    assert len(channels_json['all_members']) == 2

    # Trying to remove user2 again from owner_members, NOT an owner_member, InputError.
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 400


def test_channel_removeowner_only_owner_member(clear_and_register_and_create):
    """
    2 owner_members of a channel,
    user1 removes user2,
    user1 tries to remove themselves,
    InputError, as the last owner_member cannot remove
    themselves as an owner.
    """
    user1_id = clear_and_register_and_create[0]
    user1_token = clear_and_register_and_create[1]
    user2_id = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[4]

    # Remove user2 as an owner, and then try and remove user1 as an owner,
    # As they are the ONLY owner left, InputError
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 200

    # User1 is the only owner Here.
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user1_id})
    assert remove.status_code == 400


# Channel ID is valid, Token is not authorised with owner permissions.
def test_channel_removeowner_not_authorised(clear_and_register_and_create):
    """
    2 owner_members of a channel,
    user3 joins the channel, 
    tries to remove user2,
    AccessError
    """
    user2_id = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[4]

    # Create user3, join them to the channel, try and remove user2 with user3's ID
    user3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc3@def.com', 'password': 'password3',
                               'name_first': 'first3', 'name_last': 'last3'})
    user3_data = user3.json()
    user3_token = user3_data['token']

    # add user3 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user3_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # Using user3's token to try and remove user2 as an owner
    # user3 is only a member, NOT an owner.
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user3_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 403



def test_channel_removeowner_bad_channel_id(clear_and_register_and_create):
    """
    Tests removeowner with all possible invalid inputs for channel_id:
        - empty string
        - string
        - int/negative int
        - boolean
    """
    user2_id = clear_and_register_and_create[2]
    user2_token = clear_and_register_and_create[3]

    # Run removeowner with all potential inputs for channel_id
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user2_token, 'channel_id': '', 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user2_token, 'channel_id': 'bad_channel_id', 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user2_token, 'channel_id': 444, 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user2_token, 'channel_id': -1, 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user2_token, 'channel_id': True, 'u_id': user2_id})
    assert remove.status_code == 400


def test_channel_removeowner_bad_user_id(clear_and_register_and_create):
    """
    Tests removeowner with all possible invalid inputs for user_id:
        - empty string
        - string
        - int/negative int
        - boolean
    Creates a 3rd user to test their id againest a channel where they
    are not a member.
    """
    user1_token = clear_and_register_and_create[1]
    channel_id = clear_and_register_and_create[4]

    # User 3 used to test a using not in the channel being removed.
    user3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc3@def.com', 'password': 'password3',
                               'name_first': 'first3', 'name_last': 'last3'})
    user3_data = user3.json()
    user3_id = user3_data['auth_user_id']

    # user2 being removed as owner_member with user1's token
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': ''})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': 'string'})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': 444})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': -1})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': True})
    assert remove.status_code == 400

    # Using an user_id of a user who isnt in the channel, (NOT in all_members or owner_members).
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user3_id})
    assert remove.status_code == 400

def test_channel_removeowner_bad_token(clear_and_register_and_create):
    """
    Tests removeowner with all possible invalid inputs for token:
        - empty string
        - string
        - int/negative int
        - boolean
        - an expired token
        - an unsave token
    """
    user2_id = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[4]

    # Run removeowner with all potential inputs for token
    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': '', 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': 'string', 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 403

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': 444, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': -1, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': True, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 400

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': expired_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 403

    remove = requests.post(config.url + 'channel/removeowner/v1', 
                        json={'token': unsaved_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert remove.status_code == 403

requests.delete(config.url + 'clear/v1')
