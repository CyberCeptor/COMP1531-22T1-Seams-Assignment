
import pytest

import requests

from src import config

@pytest.fixture
def clear_register_createdm(clear_register_two):
    """ clears any data stored in data_store, registers two users, creates a dm
    channel using the first user's id and adds the second user into it """

    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    create_dm = requests.post(config.url + 'dm/create/v1', 
                              json={'token': user1['token'],
                                    'u_ids': [user2['auth_user_id']]})
    dm = create_dm.json()
    dm_id = dm['dm_id']

    return [user1['token'], dm_id]
