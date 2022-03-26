
import pytest

import requests

from src import config

@pytest.fixture
def clear_register_create_dm(clear_and_register_two):
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    requests.delete(config.url + 'clear/v1')
    
    # user1 = clear_and_register_two[0]
    # user2 = clear_and_register_two[1]
    # create_dm = requests.post(config.url + 'dm/create/v1', 
    #                     json={'token': user1['token'], 'u_ids': [user2['auth_user_id']]})
    # dm = create_dm.json()
    # dm_id = dm['dm_id']

    # return [user1['token'], dm_id]

    # create user 1
    register_user_1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_1_data = register_user_1.json()
    token_1 = user_1_data['token']
    # create user 2
    register_user_2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    user_2_data = register_user_2.json()
    id2 = user_2_data['auth_user_id']
    # user 1 creates dm directing user 2
    create_dm = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token_1, 'u_ids': [id2]})
    dm = create_dm.json()
    dm_id = dm['dm_id']

    return [token_1, dm_id]
