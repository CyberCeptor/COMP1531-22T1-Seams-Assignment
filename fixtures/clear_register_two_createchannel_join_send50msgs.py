"""
Filename: clear_register_two_createchannel_join_send50msgs.py

Author: Aleesha Bunrith(z5371516)
Created: 28/03/2022

Description: pytest fixture for registering two users, creating a channel and 
             sending 50 messages in it that tags the second user
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register_two_createchannel_join_send50msgs(clear_register_two_createchannel):
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using token, send 50 messages to channel
    """

    user1 = clear_register_two_createchannel[0]
    user2 = clear_register_two_createchannel[1]
    channel_id = clear_register_two_createchannel[2]

    token = user1['token']

    # user2 joins the channel
    resp = requests.post(config.url + 'channel/join/v2', 
                         json={'token': user2['token'], 
                                'channel_id': channel_id})
    assert resp.status_code == STATUS_OK

    # user1 sends 50 messages tagging user2
    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': '@firstlast0 hewwo'})
    assert resp.status_code == STATUS_OK
 
    return [user1['token'], user2['token'], channel_id]
