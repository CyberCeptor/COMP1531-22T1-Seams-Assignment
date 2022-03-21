"""
Filename: channels_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_list_v1
"""

import pytest
import requests
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_list_v1
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
    create a user, create 4 channels
    create a second user, create 2 channels
    create a channel_list for user1
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
    channel1_json = channel1.json()

    channel2 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name2', 'is_public': True})
    channel2_json = channel2.json()

    # create a private channel aswell to test list. 
    channel3 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'private_channel1', 'is_public': False})
    channel3_json = channel3.json()

    # channel_list for user 1.
    channels_list = requests.get(config.url + 'channels/list', params = {'token': user1_json['token']})
    channels_list_json = channels_list.json()


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

    # creating the channel list for the second user.
    requests.get(config.url + 'channels/list', params = {'token': user2_json['token']})

    # check the channels_list function has worked.
    assert channels_list.status_code == 200
    # check the number of channels in list for user1.
    assert len(channels_list_json['channels']) == 3
    # check that the channel_list info matches what was created.
    assert channels_list_json['channels'][0]['channel_id'] == channel1_json['channel_id']
    assert channels_list_json['channels'][1]['channel_id'] == channel2_json['channel_id']
    assert channels_list_json['channels'][2]['channel_id'] == channel3_json['channel_id']
    assert channels_list_json['channels'][0]['name'] == channel1_json['name']
    assert channels_list_json['channels'][1]['name'] == channel2_json['name']
    assert channels_list_json['channels'][2]['name'] == channel3_json['name']

    assert 

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

    channels_list = requests.get(config.url + 'channels/list', params = {'token': '4444'})
    channels_list_json = channels_list.json()

    assert channels_list_json.status_code == 400

    # clear_v1()
    # user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    # id1 = user1['auth_user_id']
    # channels_create_v1(id1, 'test_channel_public', True)
    # channels_create_v1(id1, 'test_channel_private', False)
    # auth_id 1 has created two channels, there is no user 4444 to create the
    # channels list.
    # with pytest.raises(AccessError):
    #     channels_list_v1(44444) # give incorrect auth_id.





def test_channels_list_v1():
    """
    Test that the channels list is functionally with multiple channels being
    created. This also tests for public and private channels.
    Also tests that channel_list only returns the channel that the id is in.

    Arguments:  N/A

    Exceptions: N/A

    Return Value:   N/A
    """








    clear_v1()
    user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    id1 = user1['auth_user_id']
    chan1 = channels_create_v1(id1, 'test_channel_public1', True)
    chan2 = channels_create_v1(id1, 'test_channel_public2', True)
    chan3 = channels_create_v1(id1, 'test_channel_priv1', False)
    chan4 = channels_create_v1(id1, 'test_channel_priv2', False)

    # adding some random channels from another user to makes sure its not
    # returning all channels, even those which the user isnt in.
    user2 = auth_register_v1('def@abc.com', 'password', 'first', 'last')
    id2 = user2['auth_user_id']
    channels_create_v1(id2, 'test2_channel_pub', True)
    channels_create_v1(id2, 'test2_channel_priv', False)
    # returns a Dict containing 'channel_id' and 'name' of all channels the user
    # is in.
    channels_list = channels_list_v1(id1)
    channels_list_v1(id2)

    # check the first four channels in the dict, check that the channel_id
    # matches what was created.
    assert channels_list['channels'][0]['channel_id'] == chan1['channel_id']
    assert channels_list['channels'][1]['channel_id'] == chan2['channel_id']
    assert channels_list['channels'][2]['channel_id'] == chan3['channel_id']
    assert channels_list['channels'][3]['channel_id'] == chan4['channel_id']

    # Testing to make sure that only 4 channels have been created for that user.
    assert len(channels_list['channels']) == 4

clear_v1()