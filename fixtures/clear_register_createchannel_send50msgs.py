"""
Filename: clear_register_createchannel_send50msgs.py

Author: Aleesha Bunrith(z5371516)
Created: 28/03/2022

Description: pytest fixture for registering one user, creating a channel and 
             sending a message in it
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register_createchannel_send50msgs(clear_register_createchannel):
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using token, send 50 messages to channel
    """

    user_data = clear_register_createchannel[0]
    channel_id = clear_register_createchannel[1]

    token = user_data['token']

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id,
                                'message': 'hewwo'})
    assert resp.status_code == STATUS_OK
 
    return [user_data['token'], channel_id]
