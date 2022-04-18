"""
Filename: message_pin_test.py

Author: Yangjun Yue, z5317840
Created: 06/04/22

Description: pytests for
    - pin messages with given message id
"""

import pytest

import requests

from src import config
 
from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_pin_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of token """

    # token is int
    message_id = clear_register_two_createchanneldm_sendmsg[3]
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': 0, 'message_id': message_id})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is boo
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': True, 'message_id': message_id})
 
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': '', 'message_id': message_id})
 
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': 'str', 'message_id': message_id})
 
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': EXPIRED_TOKEN, 
                          'message_id': message_id})
 
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': UNSAVED_TOKEN, 
                          'message_id': message_id})
 
    assert resp5.status_code == STATUS_ACCESS_ERR
    
@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_pin_invalid_message_id(
    clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of message id """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    # no message id input
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token, 'message_id': ''})
 
    assert resp0.status_code == STATUS_INPUT_ERR
    # message id is boo
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token, 'message_id': True})
    assert resp1.status_code == STATUS_INPUT_ERR
    # message id is string
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token, 'message_id': 'str'})
    assert resp2.status_code == STATUS_INPUT_ERR
    # non-existent message id
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token, 'message_id': -1})
    assert resp3.status_code == STATUS_INPUT_ERR

    # message_id is not a valid message within a channel or DM 
    # that the authorised user has joined
    resp4 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token, 'message_id': 100})
 
    assert resp4.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_successful_message_pin_owner(
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message pin is successful by owner and input errors 
    """
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    c_message_id = clear_register_two_createchanneldm_sendmsg[3]
    d_message_id = clear_register_two_createchanneldm_sendmsg[5]

    # successful pin by user1 who is owner member
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_1, 'message_id': c_message_id})
    assert resp0.status_code == STATUS_OK

    # user 1 tries to pin the message
    # input error when message is already pinned
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_1, 'message_id': c_message_id})
    assert resp1.status_code == STATUS_INPUT_ERR

    # successful pin of dm message
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_1, 'message_id': d_message_id})
    assert resp2.status_code == STATUS_OK

    # user 1 tries to pin the dm message
    # input error when message is already pinned
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_1, 'message_id': d_message_id})
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_fail_message_pin_not_owner(clear_register_two_createchanneldm_sendmsg):
    """ testing if message pin fails when user is not owner """

    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    c_message_id = clear_register_two_createchanneldm_sendmsg[3]
    d_message_id = clear_register_two_createchanneldm_sendmsg[5]

    # register user3
    resp0 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'ghu@jkl.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == STATUS_OK
    token_3 = resp0.json()['token']

    # user3 is not a member of the channel
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_3, 'message_id': c_message_id})
    assert resp1.status_code == STATUS_ACCESS_ERR

    # user2 is a member but not a global owner
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_2, 'message_id': c_message_id})
    assert resp2.status_code == STATUS_ACCESS_ERR

    # user2 is in dm but not the creator
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json={'token': token_2, 'message_id': d_message_id})
    assert resp3.status_code == STATUS_ACCESS_ERR

requests.delete(config.url + 'clear/v1')
