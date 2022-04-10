"""
Filename: clear_register_two_createchanneldm_sendmsg.py

Author: Yangjun Yue(z5317840)
Created: 27/03/2022

Description: pytest fixture for registering two users, creating a channel and a
             dm, and sending a message in each
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register_two_createchanneldm_sendmsg(clear_register_two_createchanneldm):
    """ clears any data stored in data_store and registers two users with the
    given information, create a channel and dm using token, send a message in 
    each """

    user_1 = clear_register_two_createchanneldm[0]
    user_2 = clear_register_two_createchanneldm[1]
    channel_id = clear_register_two_createchanneldm[2]
    dm_id = clear_register_two_createchanneldm[3]
    
    # user1 sends message in channel 1, tagging user 2
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': user_1['token'],
                                'channel_id': channel_id, 
                                'message': '@firstlast0 hewwo'})
    assert send_message.status_code == STATUS_OK
    chan_message = send_message.json()

    # user 2 sends message in dm
    send_message = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': user_2['token'],
                                'dm_id': dm_id, 
                                'message': 'hewwo'})
    assert send_message.status_code == STATUS_OK
    dm_message = send_message.json()

    return [user_1, user_2, channel_id, chan_message['message_id'], dm_id,
            dm_message['message_id']]
