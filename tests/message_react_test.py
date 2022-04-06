"""
Filename: message_react_test.py

Author: Aleesha Bunrith(z5371516)
Created: 01/04/2022

Description: pytests for message/react/v1
"""

import pytest

import requests

from src import config

"""
create two users, create a channel and dm and send messages in both, react to msg
and check return of message/react/v1
"""

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_react_successful(clear_register_two_createchanneldm_sendmsg):
    """ test a successful case """
    
    token1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_msg_id = clear_register_two_createchanneldm_sendmsg[5]

    # for a channel message
    react1 = requests.post(config.url + 'message/react/v1', 
                           json={'token': token1, 'message_id': chan_msg_id, 
                                 'react_id': 1})
    assert react1.status_code == 200
    
    msg_data = requests.get(config.url + 'channel/messages/v2', params={'token': token1, 'message_id': chan_msg_id})
    assert msg_data.status_code == 200
    msg = msg_data.json() 

    # for a dm message


@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_react_already_reacted(clear_register_two_createchanneldm_sendmsg):
    """ test that an input error is raised when the same user tries to react to 
    a message again with the same react """


@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_react_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test invalid token inputs """



@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_react_invalid_msg_id(clear_register_two_createchanneldm_sendmsg):
    """ test invalid msg id inputs """



@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_react_invalid_react_id(clear_register_two_createchanneldm_sendmsg):
    """ test invalid react id inputs """



@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_react_not_a_member(clear_register_two_createchanneldm_sendmsg):
    """ test with a user who is not in the channel or dm """


requests.delete(config.url + 'clear/v1')
