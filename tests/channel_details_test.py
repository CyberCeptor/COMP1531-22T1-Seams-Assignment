"""
Filename: channel_details_test.py

Author: Yangjun Yue(z5317840)
Created: 28/02/2022 - 27/03/2022

Description: pytests for channel_details_v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token, status_ok,\
                            status_input_err, status_access_err


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_invalid_token(clear_register_createchannel):
    """ testing invalid user type to raise input error """

    # token is int
    chan_id = clear_register_createchannel[1]
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': 0, 'channel_id': chan_id})
    assert resp0.status_code == status_input_err
    # token is boo
    resp1 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': True, 'channel_id': chan_id})
    assert resp1.status_code == status_input_err
    # token input empty
    resp2 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': '', 'channel_id': chan_id})
    assert resp2.status_code == status_input_err
    # wrong token input
    resp3 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': 'not right string',
                                  'channel_id': chan_id})
    assert resp3.status_code == status_access_err

    # expired token
    resp4 = requests.get(config.url + 'channel/details/v2', 
                         params={'token': expired_token, 'channel_id': chan_id})
    assert resp4.status_code == status_access_err

    # unsaved token
    resp5 = requests.get(config.url + 'channel/details/v2', 
                         params={'token': unsaved_token, 'channel_id': chan_id})
    assert resp5.status_code == status_access_err

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_invalid_channel(clear_register_createchannel):
    """ testing invalid channel id to raise input error """
  
    token = clear_register_createchannel[0]['token']
    # no channel id input
    resp0 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': ''})
    assert resp0.status_code == status_input_err
    # channel id is boo
    resp1 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': True})
    assert resp1.status_code == status_input_err
    # channel id is string
    resp2 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': 'str'})
    assert resp2.status_code == status_input_err
    # wrong channel input
    resp3 = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': 2})
    assert resp3.status_code == status_input_err
    
@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_user_not_belong(clear_register_createchannel):
    """ testing if user belongs to the channel """
    
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
    assert resp0.status_code == status_access_err
    
    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_details_return(clear_register_createchannel):
    """ testing if channel_details_v1 returns right values """
    
    # pylint: disable=unused-argument
    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]
    u_id = clear_register_createchannel[0]['auth_user_id']

    # success run
    resp = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': chan_id})
    assert resp.status_code == status_ok

    chan_details = resp.json()

    # check matching information
    assert chan_details['name'] == 'channel_name'
    assert chan_details['is_public'] == True

    # user 1 is the only member in this channel for now
    assert u_id in [k['u_id'] for k in chan_details['owner_members']]
    assert 'abc@def.com' in [k['email'] for k in chan_details['owner_members']]
    assert 'first' in [k['name_first'] for k in chan_details['owner_members']]
    assert 'last' in [k['name_last'] for k in chan_details['owner_members']]
    assert 'firstlast' in [k['handle_str'] for k in chan_details['owner_members']]

    assert u_id in [k['u_id'] for k in chan_details['all_members']]
    assert 'abc@def.com' in [k['email'] for k in chan_details['all_members']]
    assert 'first' in [k['name_first'] for k in chan_details['all_members']]
    assert 'last' in [k['name_last'] for k in chan_details['all_members']]
    assert 'firstlast' in [k['handle_str'] for k in chan_details['all_members']]

requests.delete(config.url + 'clear/v1')

