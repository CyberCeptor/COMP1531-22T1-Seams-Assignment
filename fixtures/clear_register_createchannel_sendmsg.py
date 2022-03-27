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
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using token, send a message to channel
    """

    user_data = clear_register_createchannel[0]
    channel_id = clear_register_createchannel[1]

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': user_data['token'],
                                'channel_id': channel_id, 
                                'message': 'hewwo'})
    assert send_message.status_code == 200
    message = send_message.json()
 
    return [user_data['token'], channel_id, message['message_id']]
