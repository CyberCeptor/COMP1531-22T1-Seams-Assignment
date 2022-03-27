"""
Filename: channel_test.py

Author: Yangjun Yue(z5317840)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_details_v1
"""

import pytest

import requests

from src import config

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_invalid_token(clear_register_createchannel):
    """
    testing invalid user type to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
    # pylint: disable=unused-argument


    # token is int
    chan_id = clear_register_createchannel[1]
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': 0, 'channel_id': chan_id})
    assert resp0.status_code == 400
    # token is boo
    resp1 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': True, 'channel_id': chan_id})
    assert resp1.status_code == 400
    # token input empty
    resp2 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': '', 'channel_id': chan_id})
    assert resp2.status_code == 400
    # wrong token input
    resp3 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': 'not right string',
                                  'channel_id': chan_id})
    assert resp3.status_code == 403
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    resp4 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': expired_token, 'channel_id': chan_id})
    assert resp4.status_code == 403
    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSw\
            iaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRq\
            pQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    resp5 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': unsaved_token, 'channel_id': chan_id})
    assert resp5.status_code == 403


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_invalid_channel(clear_register_createchannel):
    """
    testing invalid channel id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A
    """
  
    token = clear_register_createchannel[0]['token']
    # no channel id input
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': ''})
    assert resp0.status_code == 400
    # channel id is boo
    resp1 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': True})
    assert resp1.status_code == 400
    # channel id is string
    resp2 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': 'str'})
    assert resp2.status_code == 400
    # wrong channel input
    resp3 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': 2})
    assert resp3.status_code == 400
    

@pytest.mark.usefixtures('clear_register_createchannel')
def test_user_not_belong(clear_register_createchannel):
    """
    testing if user belongs to the channel

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: 
        Access Error - Raised for all test cases below

    Return Value: N/A
    """
    
    chan_id = clear_register_createchannel[1]

    # create user 2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']
    # raise access error when user is not in the channel
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token_2, 'channel_id': chan_id})
    assert resp0.status_code == 403
    
    requests.delete(config.url + 'clear/v1')


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_return(clear_register_createchannel):
    """
    testing if channel_details_v1 returns right values

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    

    # pylint: disable=unused-argument
    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]
    u_id = clear_register_createchannel[0]['auth_user_id']

    # success run
    resp = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': chan_id})
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
    # user 1 is the only member in this channel for now
    assert channel_details['all_members']== owner_members

requests.delete(config.url + 'clear/v1')

