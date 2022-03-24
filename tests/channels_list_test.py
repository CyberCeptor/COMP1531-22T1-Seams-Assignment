"""
Filename: channels_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_list_v1
"""
import pytest
import requests

from src import config

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})

    data = response.json()
    token = data['token']
    return token


def test_channels_list():
    """
    Creates a 2 channels:
        -   tests if given a non-existant
        user_id it raises an accesserror
        -   tests for non-int input (bool, string)
    Arguments:  N/A

    Exceptions:
        AccessError  - raised for non-user_id
        InputError  - for non int input

    Return Value: N/A
    """

    # create 2 users, create two channels, create a channels list with the first user
    # assert:
    # the status code
    # the channels_id matches the output of the channels created
    # the number of channels created in the list "len()"
    """
    create a user, create 3 channels
    create a channel_list for user1
    create a second user, create 2 channels
    create a channel_list for user2
    check that the channel_list for user1 matches what has been created
    and the length of 4.

    """

    requests.delete(config.url + 'clear/v1')


    # create user1.
    user1 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user1_json = user1.json()

    # create the 3 channels for user1.
    channel1 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name1', 'is_public': True})

    assert channel1.status_code == 200
    channel1_json = channel1.json()


    channel2 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name2', 'is_public': True})
    channel2_json = channel2.json()

    # create a private channel aswell to test list. 
    channel3 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'private_channel1', 'is_public': False})
    channel3_json = channel3.json()

    # create user2.
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    # Public channel for other user.
    requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_json['token'], 'name': 'test_pub_channel', 'is_public': True})
    # Private channel for other user.
    requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_json['token'], 'name': 'test_pri_channel', 'is_public': False})



    # channel_list for user 1.
    channels_list = requests.get(config.url + 'channels/list/v2', params = {'token': user1_json['token']})
    channels_list_json = channels_list.json()

    # creating the channel list for the second user.
    requests.get(config.url + 'channels/list/v2', params = {'token': user2_json['token']})

    # check the channels_list function has worked.
    assert channels_list.status_code == 200
    # check the number of channels in list for user1.
    assert len(channels_list_json['channels']) == 3
    # check that the channel_list info matches what was created.
    assert channels_list_json['channels'][0]['channel_id'] == channel1_json['channel_id']
    assert channels_list_json['channels'][1]['channel_id'] == channel2_json['channel_id']
    assert channels_list_json['channels'][2]['channel_id'] == channel3_json['channel_id']
    assert channels_list_json['channels'][0]['name'] == 'channel_name1'
    assert channels_list_json['channels'][1]['name'] == 'channel_name2'
    assert channels_list_json['channels'][2]['name'] == 'private_channel1'


    # clear_v1()
    # user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    # id1 = user1['auth_user_id']
    # channels_create_v1(id1, 'test_channel', True)
    # channels_create_v1(id1, 'test_channel', False)
    # with pytest.raises(AccessError):
    #     channels_list_v1(2)
    # with pytest.raises(InputError):
    #     channels_list_v1(-2)
    # with pytest.raises(InputError):
    #     channels_list_v1(True)
    # with pytest.raises(InputError):
    #     channels_list_v1('String')
    # with pytest.raises(InputError):
    #     channels_list_v1('')

def test_channels_list_invalid_token():
    """
    Create channel, and test a non-valid id.

    Arguments: N/A

    Exceptions:
        AccessError -   for the non valid id case below

    Return Value: N/A
    """

    """
    Create a user, create two channels, give an incorrect token value to channels_list
    """
    requests.delete(config.url + 'clear/v1')

    user1 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user1_json = user1.json()

    requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'public_channel', 'is_public': True})

    requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'priv_channel', 'is_public': False})

    # passing incorrect string as token.
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': 'SomeWordsHere'})
    assert channels_list_json.status_code == 403 # AccessError

    # passing int as a token.
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': 4444})
    assert channels_list_json.status_code == 400

    # passing a True bool as a token
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': True})
    assert channels_list_json.status_code == 400

    # passing a False bool as a token
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': False})
    assert channels_list_json.status_code == 400

    # an expired token passed to channels list.
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmly\
        c3RsYXN0IiwiZXhwIjoxNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'

    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': expired_token})
    assert channels_list_json.status_code == 403


    # channels_list_json = channels_list.json()
    # assert channels_list_json.status_code == 400
    # clear_v1()
    # user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    # id1 = user1['auth_user_id']
    # channels_create_v1(id1, 'test_channel_public', True)
    # channels_create_v1(id1, 'test_channel_private', False)
    # auth_id 1 has created two channels, there is no user 4444 to create the
    # channels list.
    # with pytest.raises(AccessError):
    #     channels_list_v1(44444) # give incorrect auth_id.


# def test_channels_logout():
#     requests.delete(config.url + 'clear/v1')

#     user = requests.post(config.url + 'auth/register/v2', 
#                   json={'email': 'abc@def.com', 'password': 'password',
#                         'name_first': 'first', 'name_last': 'last'})
#     user_json = user.json()
#     logout = requests.post(config.url + 'auth/logout/v1', user_json['token'])

#     assert logout.status_code == 200

#     channel = requests.post(config.url + 'channels/create/v2', 
#                             json={'token': user_json['token'], 'name': 'public_channel', 'is_public': True})
    
#     assert channel.status_code == 403
