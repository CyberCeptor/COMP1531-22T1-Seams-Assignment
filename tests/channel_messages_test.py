"""
Filename: channel_test.py

Author: Xingjian Dong (z5221888)
Created: 28/02/2022 - 06/03/2022

Description: pytests for channel_messages_v1
"""

import pytest
import requests
from src import config

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_invalid_channel(clear_register_createchannel):
    """
    testing invalid channel id to raise input error

    Arguments: clear_register_createchannel (fixture)

    Exceptions: InputError - Raised for all test cases listed below

    Return Value: N/A
    """

    token = clear_register_createchannel[0]['token']
   
    # no channel id input
    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': '', 'start': 0})
    assert resp0.status_code == 400
    # channel id is boo
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': True, 'start': 0})
    assert resp1.status_code == 400
    # channel id is string
    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': 'not int', 'start': 0})
    assert resp2.status_code == 400
    # wrong channel input
    resp3 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': 5, 'start': 0})
    assert resp3.status_code == 400
    resp4 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': -1, 'start': 0})
    assert resp4.status_code == 400


    # # no channel id input
    # with pytest.raises(InputError):
    #     channel_messages_v1(id1, '', 0)
    # # wrong channel id input
    # with pytest.raises(InputError):
    #     channel_messages_v1(id1, -1, 0)
    # # wrong channel id input
    # with pytest.raises(InputError):
    #     channel_messages_v1(id1, 5, 0)
    # # wrong type channel id input
    # with pytest.raises(InputError):
    #     channel_messages_v1(id1, 'not int', 0)
    # # wrong type channel id input
    # with pytest.raises(InputError):
    #     channel_messages_v1(id1, True, 0)

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_invalid_token(clear_register_createchannel):
    """
    testing invalid input of token

    Arguments: clear_register_createchannel (fixture)

    Exceptions: InputError - Raised for all test cases listed below

    Return Value: N/A

    """
    chan_id = clear_register_createchannel[1]
   
    # no token input
    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': '', 'channel_id': chan_id, 'start': 0})
    assert resp0.status_code == 400
    # token is boo
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': True, 'channel_id': chan_id, 'start': 0})
    assert resp1.status_code == 400
    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': False, 'channel_id': chan_id, 'start': 0})
    assert resp2.status_code == 400
    # wrong token input
    resp3 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': 'str', 'channel_id': chan_id, 'start': 0})
    # wrong token type int                      
    assert resp3.status_code == 403
    resp4 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': 0, 'channel_id': chan_id, 'start': 0})
    assert resp4.status_code == 400
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    resp5 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': expired_token, 'channel_id': chan_id, 'start': 0})
    assert resp5.status_code == 403
    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZ\
        CI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQt\
        KmJgNLiD8eAEiTv2i8ToK3mkY'
    resp6 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': unsaved_token, 'channel_id': chan_id, 'start': 0})
    assert resp6.status_code == 403
    
    requests.delete(config.url + 'clear/v1')

    # # no user input
    # with pytest.raises(InputError):
    #     channel_messages_v1('', chan_id1, 0)
    # # wrong type user input
    # with pytest.raises(InputError):
    #     channel_messages_v1('not int', chan_id1, 0)
    # # wrong type user input
    # with pytest.raises(InputError):
    #     channel_messages_v1(True, chan_id1, 0)
    # # user is not in the channel
    # with pytest.raises(AccessError):
    #     channel_messages_v1(2, chan_id1, 0)
    # # non exist user input
    # with pytest.raises(InputError):
    #     channel_messages_v1(-1, chan_id1, 0)

# clear_v1()

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_invalid_start(clear_register_createchannel):
    '''
    testing if start is int

    Arguments: clear_register_createchannel (fixture)

    Exceptions: AccessError - Raised for all test cases listed below

    Return Value: N/A
    
    
    '''
    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]
    # start is bool
    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': True})
    assert resp0.status_code == 400
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': False})
    assert resp1.status_code == 400
    # start is str
    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': ''})
    assert resp2.status_code == 400
    resp3 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': 'str'})
    assert resp3.status_code == 400
    # start is too big or negative
    resp4 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': -5})
    assert resp4.status_code == 400
    resp5 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': 1000})
    assert resp5.status_code == 400

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_user_not_belong(clear_register_createchannel):
    """
    testing if user belongs to the channel

    Arguments: clear_register_createchannel (fixture)

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

    resp0 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token_2, 'channel_id': chan_id, 'start': True})
    assert resp0.status_code == 403

    requests.delete(config.url + 'clear/v1')
    
@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_messages_return(clear_register_createchannel):
    '''
    testing channel_message returns empty if no message

    Arguments: clear_register_createchannel (fixture)

    Exceptions: N/A

    Return Value: N/A
    
    
    '''
        # pylint: disable=unused-argument

    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    # test success run
    resp = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': chan_id, 'start': 0})
    assert resp.status_code == 200
    channel_messages = resp.json()

    assert channel_messages['messages'] == []
    assert channel_messages['start'] == 0
    assert channel_messages['end'] == -1

requests.delete(config.url + 'clear/v1')
