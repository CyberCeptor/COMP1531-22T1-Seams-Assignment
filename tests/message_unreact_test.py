"""
Filename: message_unreact_test.py

Author: Yangjun Yue (z5317840)
Created: 08/04/2022

Description: pytests for message/ununreact/v1
"""

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, EXPIRED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_unreact_successful(clear_register_two_createchanneldm_sendmsg):
    """ test a successful case """
    
    token1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    id1 = clear_register_two_createchanneldm_sendmsg[0]['auth_user_id']
    token2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    id2 = clear_register_two_createchanneldm_sendmsg[1]['auth_user_id']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_id = clear_register_two_createchanneldm_sendmsg[4]
    dm_msg_id = clear_register_two_createchanneldm_sendmsg[5]

    # user 1 reacts to channel message
    resp0 = requests.post(config.url + 'message/react/v1', 
                          json={'token': token1, 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp0.status_code == STATUS_OK

    # user 1 unreacts to that channel message
    resp0 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token1, 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp0.status_code == STATUS_OK

    # check the message details using user 1's token
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                         params={'token': token1, 'channel_id': chan_id,
                                 'start': 0})
    assert resp1.status_code == STATUS_OK
    chan_msgs = resp1.json()

    assert len(chan_msgs['messages']) == 1
    c_msg_reacts = chan_msgs['messages'][0]['reacts']

    # there is only one valid message so it will be in index 0
    assert id1 not in c_msg_reacts[0]['u_ids']
    assert id2 not in c_msg_reacts[0]['u_ids']
    assert c_msg_reacts[0]['is_this_user_reacted'] is False


    # dm case
    # user 1 reacts to dm message
    resp0 = requests.post(config.url + 'message/react/v1', 
                          json={'token': token1, 'message_id': dm_msg_id, 
                                'react_id': 1})
    assert resp0.status_code == STATUS_OK

    # user 1 unreacts to a dm message
    resp2 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token1, 'message_id': dm_msg_id, 
                                'react_id': 1})
    assert resp2.status_code == STATUS_OK

    # check the message details using user 1's token
    resp3 = requests.get(config.url + 'dm/messages/v1', 
                         params={'token': token1, 'dm_id': dm_id, 'start': 0})
    assert resp3.status_code == STATUS_OK
    dm_msgs = resp3.json()

    assert len(dm_msgs['messages']) == 1
    d_msg_reacts = dm_msgs['messages'][0]['reacts']

    assert id1 not in d_msg_reacts[0]['u_ids']
    assert d_msg_reacts[0]['is_this_user_reacted'] is False
    
    # check the message details using user 2's token
    resp4 = requests.get(config.url + 'dm/messages/v1', 
                         params={'token': token2, 'dm_id': dm_id, 'start': 0})
    assert resp4.status_code == STATUS_OK
    dm_msgs = resp4.json()
    
    msg_unreacts = dm_msgs['messages'][0]['reacts']

    assert id2 not in msg_unreacts[0]['u_ids']
    assert msg_unreacts[0]['is_this_user_reacted'] is False

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_unreact_no_react(clear_register_two_createchanneldm_sendmsg):
    """ test that an input error is raised when user tries to unreact a message
    that has no react to it"""

    token1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_msg_id = clear_register_two_createchanneldm_sendmsg[5]

    # user 1 unreacts to a channel message that has no react
    resp0 = requests.post(config.url + 'message/unreact/v1', 
                           json={'token': token1, 'message_id': chan_msg_id, 
                                 'react_id': 1})
    assert resp0.status_code == STATUS_INPUT_ERR
    
    # user 1 unreacts to a dm message
    resp2 = requests.post(config.url + 'message/unreact/v1', 
                           json={'token': token1, 'message_id': dm_msg_id, 
                                 'react_id': 1})
    assert resp2.status_code == STATUS_INPUT_ERR


@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_unreact_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test invalid token inputs """

    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]

    # token is int
    resp0 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': 0, 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is bool
    resp1 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': True, 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': '', 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp2.status_code == STATUS_INPUT_ERR

    # not a valid jwt token str
    resp3 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': 'str', 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': EXPIRED_TOKEN,
                                'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp4 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': EXPIRED_TOKEN, 
                                'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp4.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_unreact_invalid_msg_id(clear_register_two_createchanneldm_sendmsg):
    """ test invalid msg id inputs """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']

    # no message id input
    resp0 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': '', 
                                'react_id': 1})
    assert resp0.status_code == STATUS_INPUT_ERR

    # message id is bool
    resp1 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': True, 
                                'react_id': 1})
    assert resp1.status_code == STATUS_INPUT_ERR

    # message id is string
    resp2 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': 'str', 
                                'react_id': 1})
    assert resp2.status_code == STATUS_INPUT_ERR

    # non-existent message ids
    resp3 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': -1, 
                                'react_id': 1})
    assert resp3.status_code == STATUS_INPUT_ERR

    resp4 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': 100, 
                                'react_id': 1})
    assert resp4.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_unreact_invalid_react_id(clear_register_two_createchanneldm_sendmsg):
    """ test invalid unreact id inputs """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]

    # no message id input
    resp0 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': chan_msg_id, 
                                'react_id': ''})
    assert resp0.status_code == STATUS_INPUT_ERR

    # message id is bool
    resp1 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': chan_msg_id, 
                                'react_id': True})
    assert resp1.status_code == STATUS_INPUT_ERR

    # message id is string
    resp2 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': chan_msg_id, 
                                'react_id': 'str'})
    assert resp2.status_code == STATUS_INPUT_ERR

    # non-existent message ids
    resp3 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': chan_msg_id, 
                                'react_id': -1})
    assert resp3.status_code == STATUS_INPUT_ERR

    resp4 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token, 'message_id': chan_msg_id, 
                                'react_id': 100})
    assert resp4.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_unreact_not_a_member(clear_register_two_createchanneldm_sendmsg):
    """ test with a user who is not in the channel or dm """

    token2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_msg_id = clear_register_two_createchanneldm_sendmsg[5]

    # user 2 is trying to unreact to a message sent in a channel they're not a 
    # member of
    resp0 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token2, 'message_id': chan_msg_id, 
                                'react_id': 1})
    assert resp0.status_code == STATUS_ACCESS_ERR

    # register user 3
    resp1 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'ghu@jkl.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == STATUS_OK
    token3 = resp1.json()['token']

    # user 3 is trying to unreact to a message sent in a dm they're not a member 
    # of
    resp2 = requests.post(config.url + 'message/unreact/v1', 
                          json={'token': token3, 'message_id': dm_msg_id, 
                                'react_id': 1})
    assert resp2.status_code == STATUS_ACCESS_ERR

requests.delete(config.url + 'clear/v1')
