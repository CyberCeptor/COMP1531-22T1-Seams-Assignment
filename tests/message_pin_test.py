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

from src.global_vars import expired_token, unsaved_token


@pytest.mark.usefixtures('clear_register_createchanneldm_sendmsg')
def test_message_pin_invalid_token(clear_register_createchanneldm_sendmsg):
    """ test for invalid input of token """

    # token is int
    message_id = clear_register_createchanneldm_sendmsg[2]
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': 0, 'message_id': message_id})
    assert resp0.status_code == 400

    # token is boo
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': True, 'message_id': message_id})
    assert resp1.status_code == 400

    # token input empty
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': '', 'message_id': message_id})
    assert resp2.status_code == 400

    # wrong token input
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': 'str', 'message_id': message_id})
    assert resp3.status_code == 403

    # expired token
    resp4 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': expired_token, 
                          'message_id': message_id})
    assert resp4.status_code == 403

    # unsaved token
    resp5 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': unsaved_token, 
                          'message_id': message_id})
    assert resp5.status_code == 403
    
@pytest.mark.usefixtures('clear_register_createchanneldm_sendmsg')
def test_message_pin_invalid_message_id(\
    clear_register_createchanneldm_sendmsg):
    """ test for invalid input of message id """

    token = clear_register_createchanneldm_sendmsg[0]
    # no message id input
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token, 'message_id': ''})
    assert resp0.status_code == 400
    # message id is boo
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token, 'message_id': True})
    assert resp1.status_code == 400
    # message id is string
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token, 'message_id': 'str'})
    assert resp2.status_code == 400
    # non-existent message id
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token, 'message_id': -1})
    assert resp3.status_code == 400
    # message_id is not a valid message within a channel or DM 
    # that the authorised user has joined
    resp4 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token, 'message_id': 100})
    assert resp4.status_code == 400


@pytest.mark.usefixtures('clear_register_createchanneldm_sendmsg')
def test_successful_message_pin_owner(clear_register_createchanneldm_sendmsg):
    """ testing if message pin is successful by owner and input errors 
    """
    token_1 = clear_register_createchanneldm_sendmsg[0]
    c_message_id = clear_register_createchanneldm_sendmsg[2]
    d_message_id = clear_register_createchanneldm_sendmsg[3]

    # successful pin by user1 who is owner member
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_1, 'message_id': c_message_id})
    assert resp0.status_code == 200

    # user 1 tries to pin the message
    # input error when message is already pinned
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_1, 'message_id': c_message_id})
    assert resp1.status_code == 400

    # successful pin of dm message
    resp2 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_1, 'message_id': d_message_id})
    assert resp2.status_code == 200

    # user 1 tries to pin the dm message
    # input error when message is already pinned
    resp3 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_1, 'message_id': d_message_id})
    assert resp3.status_code == 400

@pytest.mark.usefixtures('clear_register_createchanneldm_sendmsg')
def test_fail_message_pin_not_owner(clear_register_createchanneldm_sendmsg):
    """ testing if message pin fails when user is not owner 
    """
    channel_id = clear_register_createchanneldm_sendmsg[1]
    token_2 = clear_register_createchanneldm_sendmsg[4]
    c_message_id = clear_register_createchanneldm_sendmsg[2]
    d_message_id = clear_register_createchanneldm_sendmsg[3]

    # failed message pin by user2 who is not member
    resp = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_2, 'message_id': c_message_id})
    assert resp.status_code == 403

    # user 2 joins the channel 1
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_2,
                        'channel_id': channel_id})

    # failed message pin by user2 who is not owner member
    resp0 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_2, 'message_id': c_message_id})
    assert resp0.status_code == 403

    # fail pin of dm message user 2 is not owner
    resp1 = requests.post(config.url + 'message/pin/v1', 
                          json = {'token': token_2, 'message_id': d_message_id})
    assert resp1.status_code == 403