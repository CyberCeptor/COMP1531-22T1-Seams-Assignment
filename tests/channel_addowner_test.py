import pytest
import requests
import json
from src.auth import auth_register_v1
from src.user import user_profile_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src import config

@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data1 = user1.json()
    token1 = user_data1['token']

    user2 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc2@def.com', 'password': 'password2',
                               'name_first': 'first2', 'name_last': 'last2'})
    user_data2 = user2.json()
    user_id2 = user_data2['auth_user_id']
    user_token2 = user_data2['token']

    channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': token1, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = channel.json()
    channel_id = channel_data['channel_id']
    return [token1, user_id2, user_token2, channel_id]



def test_channel_addowner_bad_channel_id(clear_and_register_and_create):
    user1_token = clear_and_register_and_create[0]
    user2_id = clear_and_register_and_create[1]
    user2_token = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[3]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user2 to be an owner, with a bad channel_id
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': 444, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': -4, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': True, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': '', 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': 'string', 'u_id': user2_id})
    assert addowner.status_code == 400


def test_channel_addowner_bad_user_id(clear_and_register_and_create):
    user2_token = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[3]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user2 to be an owner, with a bad user_id
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': 444})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': True})
    assert addowner.status_code == 400  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': False})
    assert addowner.status_code == 400  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': -1})
    assert addowner.status_code == 400  
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': 'string'})
    assert addowner.status_code == 400  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': ''})
    assert addowner.status_code == 400  


def test_channel_addowner_not_a_member(clear_and_register_and_create):
    """
    Trying to addowner a user who is not a member of that channel.
    """
    user1_token = clear_and_register_and_create[0]
    user2_id = clear_and_register_and_create[1]
    channel_id = clear_and_register_and_create[3]
    
    # Adding user2 to the channel, but user1 is the only member. (i.e. user2 not a member)
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400



def test_channel_addowner_already_an_owner(clear_and_register_and_create):
    user1_token = clear_and_register_and_create[0]
    user2_id = clear_and_register_and_create[1]
    user2_token = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[3]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user2 to be an owner.
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 200

    # add user2 to be an owner AGAIN. InputError
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400


def test_channel_addowner_not_authorised(clear_and_register_and_create):
    user2_id = clear_and_register_and_create[1]
    user2_token = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[3]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user2 to be an owner, with its own token, NOT Authorised to do so. AccessError
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 403

    # Random user who isnt a member of the channel
    user3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data3 = user3.json()
    user3_token = user_data3['token']

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user3_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 403


def test_channel_addowner_bad_tokens(clear_and_register_and_create):
    user2_id = clear_and_register_and_create[1]
    user2_token = clear_and_register_and_create[2]
    channel_id = clear_and_register_and_create[3]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == 200

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': -1, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': '', 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': 'string', 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': True, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': False, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 400


def test_channel_addowner_working(clear_and_register_and_create):
    """
    Creates 2 users, creates a channel with user 1,
    adds user2 to the channel,
    calls addowner with user1 token and user2 id to make user2 an owner.
    """
    user1_token = clear_and_register_and_create[0]
    user2_id = clear_and_register_and_create[1]
    channel_id = clear_and_register_and_create[3]

    # add user2 to be an owner.
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 'u_id': user2_id})
    assert addowner.status_code == 200

    # check the data in the channel is correct
    channels_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1_token, 'channel_id': channel_id})
    channels_json = channels_details.json()

    # assert the data in channels_dict matches what was given.
    assert len(channels_json['owner_members']) == 2
    assert channels_json['owner_members'][1]['u_id'] == user2_id
    assert channels_json['owner_members'][1]['email'] == 'abc2@def.com'
    assert channels_json['owner_members'][1]['name_first'] == 'first2'
    assert channels_json['owner_members'][1]['name_last'] == 'last2'
    assert channels_json['owner_members'][1]['handle_str'] == 'first2last2'






