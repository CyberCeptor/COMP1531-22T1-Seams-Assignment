"""
Filename: standup_active_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http test for standup_active
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK, STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_standup_active_valid(clear_register_createchannel):
    """
    clears any data stored in data_store and registers users with the
    given information, test standup active function valid
    """
    user1 = clear_register_createchannel[0]
    token = user1['token']
    channel_id = clear_register_createchannel[1]
    
    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token, 'channel_id': channel_id})
    assert stand.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register')
def test_standup_active_invalid_channel(clear_register):
    """
    clears any data stored in data_store and registers users with the
    given information, a input error raised by invalid channel
    """
    user1 = clear_register
    token = user1['token']
    
    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token, 'channel_id': 44})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token, 'channel_id': -44})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token, 'channel_id': True})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token, 'channel_id': ''})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token, 'channel_id': 'sjhd'})
    assert stand.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_standup_active_is_not_in_channel(clear_register_two):
    """
    clears any data stored in data_store and registers users with the
    given information, a access error raised by user is not in channel
    """
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]
    token1 = user1['token']
    token2 = user2['token']
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': token1, 'name': 'channel_name',
                            'is_public': True})
    chan_data = chan.json()
    channel_id = chan_data['channel_id']

    stand = requests.get(config.url + 'standup/active/v1', 
                        params={'token': token2, 'channel_id': channel_id})
    assert stand.status_code == STATUS_ACCESS_ERR

requests.delete(config.url + 'clear/v1')