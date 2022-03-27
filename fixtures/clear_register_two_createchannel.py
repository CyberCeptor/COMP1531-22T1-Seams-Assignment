import pytest

import requests

from src import config

@pytest.fixture
def clear_register_two_createchannel(clear_register_two):
    """ clears any data stored in data_store, registers two users, creates a dm
    channel using the first user's id and adds the second user into it """

    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': user1['token'], 'name': 'channel_name',
                            'is_public': True})

    chan_data = chan.json()

    return [user1, user2, chan_data['channel_id']]