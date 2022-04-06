"""
Filename: clear_register_createdm_sendmsg.py

Author: Yangjun Yue(z5317840)
Created: 28/03/2022

Description: pytest fixture for registering two users, creating a dm, and
             send a message
"""

import pytest

import requests

from src import config

@pytest.fixture
def clear_register_createdm_sendmsg(clear_register_two_createdm):
    """ clears any 1 stored in 1_store and registers a user with the
    given information, create a channel using token, send a message to channel
    """

    user_1 = clear_register_two_createdm[0]
    user2 = clear_register_two_createdm[1]
    dm_id = clear_register_two_createdm[2]
 
    # user 2 sends message in dm
    send_message = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': user2['token'],
                                'dm_id': dm_id, 
                                'message': 'hewwo'})
    assert send_message.status_code == 200
    dm_message = send_message.json()

    return [user_1['token'], user2['token'], dm_message['message_id'], dm_id]