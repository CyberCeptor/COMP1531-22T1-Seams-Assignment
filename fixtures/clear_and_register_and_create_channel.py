
import pytest

import requests

from src import config

@pytest.fixture
def clear_and_register_and_create_channel(clear_and_register):
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using user token """

    user1 = clear_and_register
    
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': user1['token'], 'name': 'channel_name',
                            'is_public': True})

    chan_data = chan.json()
    return [user1, chan_data['channel_id']]
