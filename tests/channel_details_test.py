"""
Filename: channel_test.py

Author: Yangjun Yue(z5317840)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_details_v1
"""

import pytest
import requests

from src import config

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
    u_id = user_data['auth_user_id']
    resp0 = requests.post(config.url + 'channels/create/v2',
                            json={'token': token, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = resp0.json()
    channel_id = channel_data['channel_id']
    return [token, channel_id, u_id]




def test_channel_details_invalid_token(clear_and_register_and_create):
    """
    testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    # pylint: disable=unused-argument


    # token is int
    chan_id = clear_and_register_and_create[1]
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': 0, 'channel_id': chan_id})
    assert resp0.status_code == 400
    # token is boo
    resp1 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': True, 'channel_id': chan_id})
    assert resp1.status_code == 400
    # token input empty
    resp2 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': '', 'channel_id': chan_id})
    assert resp2.status_code == 400
    # wrong token input
    resp3 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': 'not right string', 'channel_id': chan_id})
    assert resp3.status_code == 403
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    resp4 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': expired_token, 'channel_id': chan_id})
    assert resp4.status_code == 403
    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSw\
            iaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRq\
            pQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    resp5 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': unsaved_token, 'channel_id': chan_id})
    assert resp5.status_code == 403

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
  
    # # no channel id input
    # with pytest.raises(InputError):
    #     channel_details_v1(id1, '')
    # # wrong channel id input
    # with pytest.raises(InputError):
    #     channel_details_v1(id1, -1)
    # # wrong type channel id input
    # with pytest.raises(InputError):
    #     channel_details_v1(id1, 'not int')
    # # non-existant channel
    # with pytest.raises(InputError):
    #     channel_details_v1(id1, 6)
    # # wrong type channel id input
    # with pytest.raises(InputError):
    #     channel_details_v1(id1, True)
  
    token = clear_and_register_and_create[0]
    # no channel id input
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': token, 'channel_id': ''})
    assert resp0.status_code == 400
    # channel id is boo
    resp1 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': token, 'channel_id': True})
    assert resp1.status_code == 400
    # channel id is string
    resp2 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': token, 'channel_id': 'str'})
    assert resp2.status_code == 400
    # wrong channel input
    resp3 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': token, 'channel_id': 2})
    assert resp3.status_code == 400
    
def test_user_not_belong(clear_and_register_and_create):
    """
    testing if user belongs to the channel

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: 
        Access Error - Raised for all test cases below

    Return Value: N/A
    """
    
    chan_id = clear_and_register_and_create[1]

    # create user 2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']

    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': token_2, 'channel_id': chan_id})
    assert resp0.status_code == 403
    
    requests.delete(config.url + 'clear/v1')


def test_channel_details_return(clear_and_register_and_create):
    """
    testing if channel_details_v1 returns right values

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    

    # pylint: disable=unused-argument
    token = clear_and_register_and_create[0]
    chan_id = clear_and_register_and_create[1]
    u_id = clear_and_register_and_create[2]

    # success run
    resp = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': token, 'channel_id': chan_id})
    assert resp.status_code == 200

    channel_details = resp.json()
    owner_members = [{
            'u_id': u_id,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast'
        }]

    # check matching information
    assert channel_details['name'] == 'channel_name'
    assert channel_details['is_public'] == True
    assert channel_details['owner_members'] == owner_members
    assert channel_details['all_members']== owner_members

    
    # assert result == {
    #     'name': 'channel_name',
    #     'is_public': True,
    #     'owner_members': [{
    #         'u_id': id1,
    #         'email': 'abc@def.com',
    #         'name_first': 'first',
    #         'name_last': 'last',
    #         'handle_str': 'firstlast'
    #     }],
    #     'all_members': [{
    #         'u_id': id1,
    #         'email': 'abc@def.com',
    #         'name_first': 'first',
    #         'name_last': 'last',
    #         'handle_str': 'firstlast'
    #     }]
    # }
