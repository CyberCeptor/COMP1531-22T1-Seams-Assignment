"""
Filename: users_stats_test.py

Author: Jenson Morgan (z5360181)

Created: 15/04/2022

Description: pytests for users/stats/v1

"""

from psutil import STATUS_LOCKED
import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR


@pytest.mark.usefixtures('clear_register_two')
def test_users_stats_working(clear_register_two):
    """
    Testing the uploadphoto works correctly, changes the users profile picture accordingly.
    """
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]
    user1_id = user1['auth_user_id']
    user2_id = user2['auth_user_id']
    user1_token = user1['token']

    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': user1_token})
    assert stats.status_code == STATUS_OK

    assert len(stats['channels_joined']) == 0
    assert len(stats['dms_joined']) == 0
    assert len(stats['messages_sent']) == 0
    assert len(stats['utilization_rate']) == 0

    # Create a channel 
    channel1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': user1_token, 'name': 'test_channel_public',
                                'is_public': True})
    assert channel1.status_code == STATUS_OK

    # Create a DM
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': user1_token, 'u_ids': [user1_id,user2_id]})
    assert create.status_code == STATUS_OK

    #Send a message in the DM.
    message_send = requests.post(config.url + 'message/send/v1', 
                          json = {'token': user1_token, 'channel_id': channel1['channel_id'], 
                          'message': 'helloworld'})
 
    assert message_send.status_code == STATUS_OK

    # Get the stats again
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': user1_token})
    assert stats.status_code == STATUS_OK

    assert len(stats['channels_joined']) == 1
    assert len(stats['dms_joined']) == 1
    assert len(stats['messages_sent']) == 1
    assert len(stats['utilization_rate']) == 1



@pytest.mark.usefixtures('clear_register')
def test_users_stats_invalid_token(clear_register):
    user = clear_register
    user1_token = user['token']
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': user1_token})
    assert stats.status_code == STATUS_OK

    # Empty String
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': ''})
    assert stats.status_code == STATUS_INPUT_ERR

    #String
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': 'token'})
    assert stats.status_code == STATUS_ACCESS_ERR

    # Expired Token
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': EXPIRED_TOKEN})
    assert stats.status_code == STATUS_ACCESS_ERR

    # Unsaved Token
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': UNSAVED_TOKEN})
    assert stats.status_code == STATUS_ACCESS_ERR

    # INT
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': 100})
    assert stats.status_code == STATUS_INPUT_ERR

    # Negative INT
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': -1})
    assert stats.status_code == STATUS_INPUT_ERR

    # Bool
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': True})
    assert stats.status_code == STATUS_INPUT_ERR

    # Bool
    stats = requests.get(config.url + 'users/stats/v1', 
                    json={'token': False})
    assert stats.status_code == STATUS_INPUT_ERR