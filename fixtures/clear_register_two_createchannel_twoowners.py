"""
Filename: clear_register_two_createchannel_twoowners.py

Author: Aleesha Bunrith(z5371516), Jenson Morgan(z5360181)
Created: 28/03/2022

Description: pytest fixture for registering two users, creating a channel, and
             adding the second user as an owner
"""

import pytest

import requests

from src import config

@pytest.fixture
def clear_register_two_createchannel_twoowners(clear_register_two_createchannel):
    """ clears any data stored in data_store, registers two users, creates a
    channel using the first user's token and adds the second user as an owner
    """

    user1 = clear_register_two_createchannel[0]
    user2 = clear_register_two_createchannel[1]
    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2['token'],
                              'channel_id': channel_id})
    assert channel_join.status_code == 200

    # add user2 to be an owner, with user1's token as they are owner_member
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1['token'], 
                              'channel_id': channel_id,
                              'u_id': user2['auth_user_id']})
    assert addowner.status_code == 200

    return [user1, user2, channel_id]