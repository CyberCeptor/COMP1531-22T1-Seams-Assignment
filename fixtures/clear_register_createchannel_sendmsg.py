import pytest

import requests

from src import config

@pytest.fixture
def clear_register_createchannel_sendmsg(clear_register_createchannel):
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id, send a message to channel
    """

    user_data = clear_register_createchannel[0]
    channel_id = clear_register_createchannel[1]

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': user_data['token'],
                                'channel_id': channel_id, 
                                'message': 'hewwo'})
    message = send_message.json()
 
    return [user_data['token'], channel_id, message['message_id']]
