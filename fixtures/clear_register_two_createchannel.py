"""
Filename: clear_register_two_createchannel.py

Author: Aleesha Bunrith(z5371516)
Created: 27/03/2022

Description: pytest fixture for registering two users and creating a channel
"""

import pytest

import requests

from src import config

@pytest.fixture
def clear_register_two_createchannel(clear_register_two):
    """ clears any data stored in data_store, registers two users, creates a
    channel using the first user's token """

    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': user1['token'], 'name': 'channel_name',
                            'is_public': True})
    assert chan.status_code == 200
    chan_data = chan.json()

    return [user1, user2, chan_data['channel_id']]