"""
Filename: channels_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_list_v1
"""
import pytest
import requests

from src import config
from src.global_vars import expired_token, unsaved_token


def test_channels_list():
    """
    Create 2 users,
    user1 creates 3 channels,
    user2 creates 2 channels, 
    user2 joins user1's first channel,
    assert that all information of returned by channels_list
    matches the above information.
    The channel_list will be in the order of lowest channel_id to 
    greatest.

    Arguments:  N/A

    Exceptions:
        AccessError  - raised for non-user_id
        InputError  - for non int input

    Return Value: N/A
    """



    requests.delete(config.url + 'clear/v1')


    # create user1.
    user1 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user1_json = user1.json()

    # create channel1 (Public)
    channel1 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name1', 'is_public': True})
    assert channel1.status_code == 200
    channel1_json = channel1.json()
    
    # create channel2 (Public)
    channel2 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name2', 'is_public': True})
    assert channel2.status_code == 200
    channel2_json = channel2.json()

    # create channel3 (Private)
    channel3 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'private_channel1', 'is_public': False})
    assert channel3.status_code == 200
    channel3_json = channel3.json()


    # create user2.
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    
    # Create channel4 for user2 (Public)
    channel4 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_json['token'], 'name': 'test_pub_channel', 'is_public': True})
    assert channel4.status_code == 200
    channel4_json = channel4.json()

    # Create channel5 for user2 (Private)
    channel5 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_json['token'], 'name': 'test_pri_channel', 'is_public': False})
    assert channel5.status_code == 200
    channel5_json = channel5.json()

    # User2 joins user1's first channels
    join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_json['token'],
                        'channel_id': channel1_json['channel_id']})
    assert join.status_code == 200   

    # Channel_list for user 1.
    channels_list = requests.get(config.url + 'channels/list/v2', params = {'token': user1_json['token']})
    assert channels_list.status_code == 200
    channels_list_json = channels_list.json()

    # Creating the channel list for the user2. Test if it interefere's with user1's list.
    channels_list2 = requests.get(config.url + 'channels/list/v2', params = {'token': user2_json['token']})
    assert channels_list2.status_code == 200
    channels_list2_json = channels_list2.json()

    # Check that the channel_list info matches what was created.
    assert len(channels_list_json['channels']) == 3
    assert channels_list_json['channels'][0]['channel_id'] == channel1_json['channel_id']
    assert channels_list_json['channels'][1]['channel_id'] == channel2_json['channel_id']
    assert channels_list_json['channels'][2]['channel_id'] == channel3_json['channel_id']
    assert channels_list_json['channels'][0]['name'] == 'channel_name1'
    assert channels_list_json['channels'][1]['name'] == 'channel_name2'
    assert channels_list_json['channels'][2]['name'] == 'private_channel1'

    '''Check that the channel_list2 info matches that was created.
     The channels_list will return in the order of channel_id, so the lowest channel_id, 
     will be the first in the list'''
    assert len(channels_list2_json['channels']) == 3
    assert channels_list2_json['channels'][0]['channel_id'] == channel1_json['channel_id']
    assert channels_list2_json['channels'][1]['channel_id'] == channel4_json['channel_id']   
    assert channels_list2_json['channels'][2]['channel_id'] == channel5_json['channel_id'] 
    
    assert channels_list2_json['channels'][0]['name'] == 'channel_name1'
    assert channels_list2_json['channels'][1]['name'] == 'test_pub_channel'
    assert channels_list2_json['channels'][2]['name'] == 'test_pri_channel'


def test_channels_list_invalid_token():
    """
    Creates 2 channels for a user,
    tries to create c channel_list with all possible invalid token's

    Arguments: N/A

    Exceptions:
        AccessError -   when channels_list is passed a string and an empty string
                    -   when passed an expired/unsaved token

        InputError  -    for all other cases (ints, -ints, and booleans)

    Return Value: N/A
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

    # passing incorrect string as token.
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': ''})
    assert channels_list_json.status_code == 403 # AccessError

    # passing int as a token.
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': 4444})
    assert channels_list_json.status_code == 400

    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': -1})
    assert channels_list_json.status_code == 400
    # passing a True bool as a token
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': True})
    assert channels_list_json.status_code == 400

    # passing a False bool as a token
    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': False})
    assert channels_list_json.status_code == 400

    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': expired_token})
    assert channels_list_json.status_code == 403

    channels_list_json = requests.get(config.url + 'channels/list/v2', params = {'token': unsaved_token})
    assert channels_list_json.status_code == 403

requests.delete(config.url + 'clear/v1')
