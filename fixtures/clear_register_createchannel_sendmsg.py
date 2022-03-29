"""
Filename: clear_register_createchannel_sendmsg.py

Author: Yangjun Yue(z5317840)
Created: 27/03/2022

Description: pytest fixture for registering one user, creating a channel and 
             sending a message in it
"""

import pytest

import requests

from src import config

@pytest.fixture
def clear_register_createchannel_sendmsg(clear_register_createchannel):
    """ clears any 1 stored in 1_store and registers a user with the
    given information, create a channel using token, send a message to channel
    """

    user_1 = clear_register_createchannel[0]
    channel_id = clear_register_createchannel[1]
    # user1 sends message in channel 1
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': user_1['token'],
                                'channel_id': channel_id, 
                                'message': 'hewwo'})
    assert send_message.status_code == 200
    chan_message = send_message.json()
 
    #create user 2 for dm create
    resp = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp.status_code == 200
    user2 = resp.json()
    # create dm for user 1 and 2
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': user_1['token'], 'u_ids': [user2['auth_user_id']]})
    assert create.status_code == 200
    dm = create.json()
    # user 2 sends message in dm
    send_message = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': user2['token'],
                                'dm_id': dm['dm_id'], 
                                'message': 'hewwo'})
    assert send_message.status_code == 200
    dm_message = send_message.json()

    return [user_1['token'], channel_id, chan_message['message_id'], dm_message['message_id'], user2['token'], dm['dm_id']]
