"""
Filename: user_stats_test.py

Author: Jenson Morgan (z5360181)

Created: 15/04/2022

Description: pytests for user/stats/v1

"""

import pytest

import requests
from fixtures.clear_register import clear_register

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR


@pytest.mark.usefixtures('clear_register_two')
def test_user_stats_working(clear_register_two):
    """
    
    """
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]
    user2_id = user2['auth_user_id']
    user1_token = user1['token']

    # Initial assert to make sure the data_store is created correctly.
    stats_return = requests.get(config.url + 'user/stats/v1', 
                    params={'token': user1_token})
    assert stats_return.status_code == STATUS_OK
    stats = stats_return.json()['user_stats']

    assert 0 in [k['num_channels_joined'] for k in stats['channels_joined']]
    assert 0 in [k['num_dms_joined'] for k in stats['dms_joined']]
    assert 0 in [k['num_messages_sent'] for k in stats['messages_sent']]
    assert stats['involvement_rate'] == 0.0

    # Create a channel 
    channel1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': user1_token, 'name': 'test_channel_public',
                                'is_public': True})
    assert channel1.status_code == STATUS_OK
    channel = channel1.json()

    # Create a DM
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': user1_token, 'u_ids': [user2_id]})
    assert create.status_code == STATUS_OK

    #Send a message in the DM.
    message_send = requests.post(config.url + 'message/send/v1', 
                          json = {'token': user1_token, 'channel_id': channel['channel_id'], 
                          'message': 'helloworld'})
    assert message_send.status_code == STATUS_OK

    # Checking that the user_stats dictionary has the information above
    # New channel, DM, message sent, and updated involvement_rate
    stats_return = requests.get(config.url + 'user/stats/v1', 
                    params={'token': user1_token})
    assert stats_return.status_code == STATUS_OK
    stats = stats_return.json()['user_stats']

    assert 1 in [k['num_channels_joined'] for k in stats['channels_joined']]
    assert 1 in [k['num_dms_joined'] for k in stats['dms_joined']]
    assert 1 in [k['num_messages_sent'] for k in stats['messages_sent']]
    assert stats['involvement_rate'] == 1.0


@pytest.mark.usefixtures('clear_register')
def test_user_stats_invalid_token(clear_register):
    user = clear_register
    user1_token = user['token']
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': user1_token})
    assert stats.status_code == STATUS_OK

    # Empty String
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': ''})
    assert stats.status_code == STATUS_INPUT_ERR

    #String
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': 'token'})
    assert stats.status_code == STATUS_ACCESS_ERR

    # Expired Token
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': EXPIRED_TOKEN})
    assert stats.status_code == STATUS_ACCESS_ERR

    # Unsaved Token
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': UNSAVED_TOKEN})
    assert stats.status_code == STATUS_ACCESS_ERR

    # INT
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': 100})
    assert stats.status_code == STATUS_INPUT_ERR

    # Negative INT
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': -1})
    assert stats.status_code == STATUS_INPUT_ERR

    # Bool
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': True})
    assert stats.status_code == STATUS_INPUT_ERR

    # Bool
    stats = requests.get(config.url + 'user/stats/v1', 
                    params={'token': False})
    assert stats.status_code == STATUS_INPUT_ERR