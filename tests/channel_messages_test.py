"""
Filename: channel_meesages_test.py

Author: Yangjun Yue(z5317840), Xingjian Dong (z5221888)
Created: 28/02/2022 - 28/03/2022

Description: pytests for channel_messages_v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token, status_ok,\
                            status_access_err, status_input_err

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_invalid_channel(clear_register_createchannel):
    """ testing invalid channel id to raise input error """

    token = clear_register_createchannel[0]['token']
   
    # no channel id input
    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': '', 
                                    'start': 0})
    assert resp0.status_code == status_input_err

    # channel id is boo
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': True, 
                                    'start': 0})
    assert resp1.status_code == status_input_err

    # channel id is string
    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': 'not int', 
                                    'start': 0})
    assert resp2.status_code == status_input_err

    # wrong channel input
    resp3 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': 5, 
                                    'start': 0})
    assert resp3.status_code == status_input_err

    resp4 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': -1, 
                                    'start': 0})
    assert resp4.status_code == status_input_err

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_invalid_token(clear_register_createchannel):
    """ testing invalid input of token """

    chan_id = clear_register_createchannel[1]
   
    # no token input
    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': '', 'channel_id': chan_id, 
                                    'start': 0})
    assert resp0.status_code == status_input_err

    # token is boo
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': True, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp1.status_code == status_input_err

    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': False, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp2.status_code == status_input_err

    # wrong token input
    resp3 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': 'str', 'channel_id': chan_id, 
                                    'start': 0})

    # wrong token type int                      
    assert resp3.status_code == status_access_err
    resp4 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': 0, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp4.status_code == status_input_err

    # expired token
    resp5 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': expired_token, 
                                    'channel_id': chan_id, 'start': 0})
    assert resp5.status_code == status_access_err

    # unsaved token
    resp6 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': unsaved_token, 
                                    'channel_id': chan_id, 'start': 0})
    assert resp6.status_code == status_access_err
    
    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_invalid_start(clear_register_createchannel):
    """ testing if start is int """
    
    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    # start is bool
    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': True})
    assert resp0.status_code == status_input_err

    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': False})
    assert resp1.status_code == status_input_err

    # start is str
    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': ''})
    assert resp2.status_code == status_input_err

    resp3 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': 'str'})
    assert resp3.status_code == status_input_err

    # start is too big or negative
    resp4 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': -5})
    assert resp4.status_code == status_input_err

    resp5 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': 1000})
    assert resp5.status_code == status_input_err

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_user_not_belong(clear_register_createchannel):
    """ testing if user belongs to the channel  """
    
    chan_id = clear_register_createchannel[1]

    # create user 2
    user2 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']

    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token_2, 'channel_id': chan_id, 
                                    'start': True})
    assert resp0.status_code == status_access_err

    requests.delete(config.url + 'clear/v1')
    
@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_return(clear_register_createchannel):
    """ testing channel_message returns empty if no message """

    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    # test success run
    resp = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp.status_code == status_ok
    channel_messages = resp.json()

    assert channel_messages['messages'] == []
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_return_less_than_50(clear_register_createchannel):
    """ testing channel_message returns all messages if there's less than 50
    messages """

    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    # test success run
    resp = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp.status_code == status_ok
    channel_messages = resp.json()

    assert len(channel_messages['messages']) == 5
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1

@pytest.mark.usefixtures('clear_register_createchannel_send50msgs')
def test_channel_messages_return_50(clear_register_createchannel_send50msgs):
    """ testing channel_message returns empty if no message """

    token = clear_register_createchannel_send50msgs[0]
    chan_id = clear_register_createchannel_send50msgs[1]

    # test success run
    resp = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp.status_code == status_ok
    channel_messages = resp.json()

    assert len(channel_messages['messages']) == 50
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1

@pytest.mark.usefixtures('clear_register_createchannel_send50msgs')
def test_channel_messages_return_more_than_50(clear_register_createchannel_send50msgs):
    """ testing channel_message returns empty if no message """

    token = clear_register_createchannel_send50msgs[0]
    chan_id = clear_register_createchannel_send50msgs[1]

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp.status_code == status_ok

    # test success run
    resp = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 
                                    'start': 0})
    assert resp.status_code == status_ok
    channel_messages = resp.json()

    assert len(channel_messages['messages']) == 50
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == 50

requests.delete(config.url + 'clear/v1')
