import pytest

import requests

from src import config

@pytest.fixture
def clear_register_createchannel_sendmsg (clear_register_createchannel):
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id, send a message to channel
    """

    requests.delete(config.url + 'clear/v1')
    # user_data = clear_and_register_and_create_channel[0]
    # channel_id = clear_and_register_and_create_channel[1]

    # send_message = requests.post(config.url + 'message/send/v1', 
    #                       json={'token': user_data['token'], 'channel_id': channel_id, 
    #                       'message': 'hewwo'})
    # message = send_message.json()
 
    # return [user_data['token'], channel_id , message['messsage_id']]
    register = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data = register.json()
    token = user_data['token']

    create_channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': token, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = create_channel.json()
    channel_id = channel_data['channel_id'] 

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id, 
                          'message': 'hewwo'})
    message = send_message.json()
    message_id = message['message_id']
 
    return [token, channel_id, message_id]
