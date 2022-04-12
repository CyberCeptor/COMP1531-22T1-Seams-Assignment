"""
Filename: clear_register_createchannel.py

Author: Aleesha Bunrith(z5371516)
Created: 28/03/2022

Description: pytest fixture for registering one user then creating a channel
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register_createchannel(clear_register):
    """ clears any data stored in data_store and registers a user with the
    given information, create a channel using user token """

    user1 = clear_register
    
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': user1['token'], 'name': 'channel_name',
                            'is_public': True})
    assert chan.status_code == STATUS_OK
    chan_data = chan.json()
    
    return [user1, chan_data['channel_id']]
