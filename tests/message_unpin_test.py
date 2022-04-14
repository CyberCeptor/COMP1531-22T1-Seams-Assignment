# """
# Filename: message_unpin_test.py

# Author: Xingjian Dong, z5221888
# Created: 04/04/22

# Description: pytests for
#     - unpin messages with given message id
# """

# import pytest

# import requests

# from src import config

 
# from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
#                             STATUS_INPUT_ERR, STATUS_ACCESS_ERR

# @pytest.mark.usefixtures('clear_register_unpin_message')
# def test_message_unpin_invalid_token(clear_register_unpin_message):
#     """ test for invalid input of token """

#     # token is int
#     message_id = clear_register_unpin_message[3]
#     resp0 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': 0, 'message_id': message_id})
 
#     assert resp0.status_code == STATUS_INPUT_ERR

#     # token is bool
#     resp1 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': True, 'message_id': message_id})
 
#     assert resp1.status_code == STATUS_INPUT_ERR

#     # token input empty
#     resp2 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': '', 'message_id': message_id})
 
#     assert resp2.status_code == STATUS_INPUT_ERR

#     # wrong token input
#     resp3 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': 'str', 'message_id': message_id})
 
#     assert resp3.status_code == STATUS_ACCESS_ERR

#     # expired token
#     resp4 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': EXPIRED_TOKEN, 
#                           'message_id': message_id})
 
#     assert resp4.status_code == STATUS_ACCESS_ERR

#     # unsaved token
#     resp5 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': UNSAVED_TOKEN, 
#                           'message_id': message_id})
 
#     assert resp5.status_code == STATUS_ACCESS_ERR
    
# @pytest.mark.usefixtures('clear_register_unpin_message')
# def test_message_unpin_invalid_message_id(clear_register_unpin_message):
#     """ test for invalid input of message id """

#     token = clear_register_unpin_message[0]['token']
#     # no message id input
#     resp0 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token, 'message_id': ''})
 
#     assert resp0.status_code == STATUS_INPUT_ERR
#     # message id is bool
#     resp1 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token, 'message_id': True})
#     assert resp1.status_code == STATUS_INPUT_ERR
#     # message id is string
#     resp2 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token, 'message_id': 'str'})
#     assert resp2.status_code == STATUS_INPUT_ERR
#     # non-existent message id
#     resp3 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token, 'message_id': -1})
#     assert resp3.status_code == STATUS_INPUT_ERR

#     # message_id is not a valid message within a channel or DM 
#     # that the authorised user has joined
#     resp4 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token, 'message_id': 100})
 
#     assert resp4.status_code == STATUS_INPUT_ERR

# @pytest.mark.usefixtures('clear_register_unpin_message')
# def test_successful_message_unpin_owner(clear_register_unpin_message):
#     """ testing if message unpin is successful by owner and input errors 
#     """
#     token_1 = clear_register_unpin_message[0]['token']
#     c_message_id = clear_register_unpin_message[3]
#     d_message_id = clear_register_unpin_message[5]

#     # successful pin by user1 who is owner member
#     resp0 = requests.post(config.url + 'message/pin/v1', 
#                           json = {'token': token_1, 'message_id': c_message_id})
 
#     assert resp0.status_code == STATUS_OK

#     # user 1 tries to unpin the message
#     resp1 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_1, 'message_id': c_message_id})
 
#     assert resp1.status_code == STATUS_OK

#     # user 1 tries to unpin the message
#     # input error when message is already unpinned
#     resp2 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_1, 'message_id': c_message_id})
 
#     assert resp2.status_code == STATUS_INPUT_ERR

#     # successful pin of dm message
#     resp3 = requests.post(config.url + 'message/pin/v1', 
#                           json = {'token': token_1, 'message_id': d_message_id})
 
#     assert resp3.status_code == STATUS_OK

#     # user 1 tries to unpin the dm message
#     resp4 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_1, 'message_id': d_message_id})

#     assert resp4.status_code == STATUS_OK

#     # user 1 tries to unpin the dm message
#     # input error when message is already unpinned
#     resp5 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_1, 'message_id': d_message_id})

#     assert resp5.status_code == STATUS_INPUT_ERR

# @pytest.mark.usefixtures('clear_register_unpin_message')
# def test_fail_message_unpin_not_owner(clear_register_unpin_message):
#     """ testing if message unpin fails when user is not owner 
#     """
#     channel_id = clear_register_unpin_message[2]
#     token_2 = clear_register_unpin_message[1]['token']
#     c_message_id = clear_register_unpin_message[3]
#     d_message_id = clear_register_unpin_message[5]

#     # failed message unpin by user2 who is not member
#     resp = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_2, 'message_id': c_message_id})
 
#     assert resp.status_code == STATUS_ACCESS_ERR

#     # user 2 joins the channel 1
#     requests.post(config.url + 'channel/join/v2',
#                         json = {'token': token_2,
#                         'channel_id': channel_id})

#     # failed message unpin by user2 who is not owner member
#     resp0 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_2, 'message_id': c_message_id})
 
#     assert resp0.status_code == STATUS_ACCESS_ERR

#     # fail unpin of dm message user 2 is not owner
#     resp1 = requests.post(config.url + 'message/unpin/v1', 
#                           json = {'token': token_2, 'message_id': d_message_id})
 
#     assert resp1.status_code == STATUS_ACCESS_ERR

# requests.delete(config.url + 'clear/v1')
