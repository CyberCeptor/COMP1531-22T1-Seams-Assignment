import pytest

import requests

from src import config

@pytest.fixture(name='clear_register_create_channel_send_message')
def fixture_clear_register_create_channel_send_message():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id, send a message to channel

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    requests.delete(config.url + 'clear/v1')
    register = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data = register.json()

    create_channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': user_data['token'], 'name': 'channel_name',
                                    'is_public': True})
    channel_data = create_channel.json()

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': user_data['token'], 'channel_id': channel_data['channel_id'], 
                          'message': 'hewwo'})
    message = send_message.json()
 
    return [user_data['token'], channel_data['channel_id'] , message['message_id']]