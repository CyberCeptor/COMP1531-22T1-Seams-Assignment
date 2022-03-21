"""
Filename: channel_test.py

Author: Yangjun Yue(z5317840)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_details_v1
"""

import pytest
import requests

from src import config
from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channel import channel_details_v1

from src.channels import channels_create_v1


@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    # clear_v1()
    # user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    # chan1 = channels_create_v1(1, 'channel_name', True)
    # return [user1['auth_user_id'], chan1['channel_id']]
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data = resp.json()
    token = user_data['token']
    resp_2 = requests.post(config.url + 'channel/create/v2',
                            json={'token': token, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = resp_2.json()
    channel_id = channel_data['channel_id']
    return [token, channel_id]




def test_channel_details_invalid_token(clear_and_register_and_create):
    """
    testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    # pylint: disable=unused-argument


    chan_id1 = clear_and_register_and_create[1]
    resp0 = requests.post(config.url + 'channel/details/v2', 
                          json={'token': 0, 'channel_id': chan_id1})
    assert resp0.status_code == 400

    resp1 = requests.post(config.url + 'channel/details/v2', 
                          json={'token': True, 'channel_id': chan_id1})
    assert resp0.status_code == 400
    # # no user input
    # with pytest.raises(InputError):
    #     channel_details_v1('', chan_id1)
    # # wrong type user input
    # with pytest.raises(InputError):
    #     channel_details_v1('not int', chan_id1)
    # # wrong type user input
    # with pytest.raises(InputError):
    #     channel_details_v1(True, chan_id1)
    # # user is not in the channel
    # with pytest.raises(AccessError):
    #     channel_details_v1(2, chan_id1)
    # # non exist user input
    # with pytest.raises(InputError):
    #     channel_details_v1(-1, chan_id1)

def test_channel_details_invalid_channel(clear_and_register_and_create):
    """
    testing invalid channel id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    id1 = clear_and_register_and_create[0]
    # no channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, '')
    # wrong channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, -1)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, 'not int')
    # non-existant channel
    with pytest.raises(InputError):
        channel_details_v1(id1, 6)
    # wrong type channel id input
    with pytest.raises(InputError):
        channel_details_v1(id1, True)

def test_channel_details_return(clear_and_register_and_create):
    """
    testing if channel_details_v1 returns right values

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    id1 = clear_and_register_and_create[0]
    chan_id1 = clear_and_register_and_create[1]
    result = channel_details_v1(id1, chan_id1)
    assert result == {
        'name': 'channel_name',
        'is_public': True,
        'owner_members': [{
            'u_id': id1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast'
        }],
        'all_members': [{
            'u_id': id1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast'
        }]
    }

clear_v1()
