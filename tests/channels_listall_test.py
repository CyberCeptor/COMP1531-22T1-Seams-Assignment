"""
Filename: channels_test.py

Author: Yangjun Yue(5317840)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_listall_v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

def test_channels_listall_invalid_token():
    """ Testing invalid user id to raise input error  """

    requests.delete(config.url + 'clear/v1')

    # token is int
    resp0 = requests.get(config.url + 'channels/listall/v2', 
        params={'token': 0})
    assert resp0.status_code == 400

    # token is bool
    resp1 = requests.get(config.url + 'channels/listall/v2', 
        params={'token': True})
    assert resp1.status_code == 400
    
    resp2 = requests.get(config.url + 'channels/listall/v2', 
        params={'token': False})
    assert resp2.status_code == 400

    # wrong string to raise access error
    resp3 = requests.get(config.url + 'channels/listall/v2', 
        params={'token': 'str'})
    assert resp3.status_code == 403 

    # token is expired
    resp4 = requests.get(config.url + 'channels/listall/v2', 
                            params={'token': expired_token})
    assert resp4.status_code == 403
    # token is unsaved
    resp5 = requests.get(config.url + 'channels/listall/v2', 
                            params={'token': unsaved_token})
    assert resp5.status_code == 403

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channels_listall_v1_return(clear_register_two_createchannel):
    """ testing if listall returns right type of value """

    user1_token = clear_register_two_createchannel[0]['token']
    user2_token = clear_register_two_createchannel[1]['token']
    channel_id1 = clear_register_two_createchannel[2]

    channel2 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_token, 
                            'name': 'channel_name2', 'is_public': True})
    channel2_json = channel2.json()

    # 3rd channel is private
    channel3 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_token, 
                            'name': 'private_channel1', 'is_public': False})
    channel3_json = channel3.json()

    # create public channel for user2
    channel4 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_token, 
                            'name': 'pub_channel_user2', 'is_public': True})
    channel4_json = channel4.json()

    # create private channel for user2
    channel5 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_token, 
                               'name': 'pri_channel_user2', 'is_public': False})
    channel5_json = channel5.json()

    # channel_list for user 1, should return all channels
    channels_listall = requests.get(config.url + 'channels/listall/v2', 
                                        params={'token': user1_token})
    channels = channels_listall.json()

    # check the channels_list function has worked.
    assert channels_listall.status_code == 200
    # check the number of channels is all channels
    assert len(channels['channels']) == 5
    # check that the channel_list info matches what was created.
    assert channel_id1 in [k['channel_id'] for k in channels['channels']]
    assert channel2_json['channel_id'] in [k['channel_id'] for k in 
                                            channels['channels']]
    assert channel3_json['channel_id'] in [k['channel_id'] for k in 
                                           channels['channels']]
    assert channel4_json['channel_id'] in [k['channel_id'] for k in 
                                            channels['channels']]
    assert channel5_json['channel_id'] in [k['channel_id'] for k in 
                                            channels['channels']]

    assert 'channel_name' in [k['name'] for k in channels['channels']]
    assert 'channel_name2' in [k['name'] for k in channels['channels']]
    assert 'private_channel1' in [k['name'] for k in channels['channels']]
    assert 'pub_channel_user2' in [k['name'] for k in channels['channels']]
    assert 'pri_channel_user2' in [k['name'] for k in channels['channels']]
    
    # check for user 2
    channels_listall_2 = requests.get(config.url + 'channels/listall/v2',
                                        params={'token': user2_token})
    channels2 = channels_listall_2.json()

    assert channels_listall_2.status_code == 200
    # check the number of channels is all channels
    assert len(channels2['channels']) == 5
    # check that the channel_list info matches what was created.
    assert channel_id1 in [k['channel_id'] for k in channels2['channels']]
    assert channel2_json['channel_id'] in [k['channel_id'] for k in 
                                            channels2['channels']]
    assert channel3_json['channel_id'] in [k['channel_id'] for k in 
                                           channels2['channels']]
    assert channel4_json['channel_id'] in [k['channel_id'] for k in 
                                            channels2['channels']]
    assert channel5_json['channel_id'] in [k['channel_id'] for k in 
                                            channels2['channels']]
                                            
    assert 'channel_name' in [k['name'] for k in channels2['channels']]
    assert 'channel_name2' in [k['name'] for k in channels2['channels']]
    assert 'private_channel1' in [k['name'] for k in channels2['channels']]
    assert 'pub_channel_user2' in [k['name'] for k in channels2['channels']]
    assert 'pri_channel_user2' in [k['name'] for k in channels2['channels']]

requests.delete(config.url + 'clear/v1')
