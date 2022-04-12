"""
Filename: clear_register_teo_createchannel.py

Author: Yangjun Yue(z5317840)
Created: 27/03/2022

Description: pytest fixture for registering two users, creating a channel and a
             dm
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK

@pytest.fixture
def clear_register_two_createchanneldm(clear_register_two_createchannel):
    """ clears any data stored in data_store and registers two users with the
    given information, create a channel and dm using token, add user2 to the 
    channel """

    user_1 = clear_register_two_createchannel[0]
    user_2 = clear_register_two_createchannel[1]
    channel_id = clear_register_two_createchannel[2]

    # create dm for user 1 and 2
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': user_1['token'],
                              'u_ids': [user_2['auth_user_id']]})
    assert create.status_code == STATUS_OK
    dm = create.json()

    # user 1 invites user 2 into the channel
    invite = requests.post(config.url + 'channel/invite/v2', 
                           json={'token': user_1['token'], 
                                 'channel_id': channel_id, 
                                 'u_id': user_2['auth_user_id']})
    assert invite.status_code == STATUS_OK

    return [user_1, user_2, channel_id, dm['dm_id']]
