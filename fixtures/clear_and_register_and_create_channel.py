
import pytest

import requests

from src import config

@pytest.fixture
def clear_and_register_and_create_channel():
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using user token """

    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'abc@def.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    data = resp.json()
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': data['token'], 'name': 'channel_name',
                            'is_public': True})

    data1 = chan.json()
    return [data['token'], data1['channel_id'], data['auth_user_id']]
