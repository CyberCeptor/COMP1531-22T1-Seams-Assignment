"""
Filename: message_remove_test.py

Author: Yangjun Yue, z5317840
Created: 23/03/22

Description: pytests for
    - removing messages with given message id
"""

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_remove_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of token """

    # token is int
    message_id = clear_register_two_createchanneldm_sendmsg[2]
    resp0 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': 0, 'message_id': message_id})
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is boo
    resp1 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': True, 'message_id': message_id})
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': '', 'message_id': message_id})
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': 'str', 'message_id': message_id})
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': EXPIRED_TOKEN, 
                          'message_id': message_id})
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': UNSAVED_TOKEN, 
                          'message_id': message_id})
    assert resp5.status_code == STATUS_ACCESS_ERR
    
@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_remove_invalid_message_id(\
    clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of channel id """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    
    # no message id input
    resp0 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': ''})
    assert resp0.status_code == STATUS_INPUT_ERR
    # message id is boo
    resp1 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': True})
    assert resp1.status_code == STATUS_INPUT_ERR
    # message id is string
    resp2 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': 'str'})
    assert resp2.status_code == STATUS_INPUT_ERR
    # non-existent message id
    resp3 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': -1})
    assert resp3.status_code == STATUS_INPUT_ERR
    resp4 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': 100})
    assert resp4.status_code == STATUS_INPUT_ERR
    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_remove_global_user(clear_register_two_createchanneldm_sendmsg):
    """ testing if global owner cannot remove message if not in that channel """
    
    # user 1 is global owner
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # user2 creates private channel 2 and becomes owner of that channel
    create_channel_2 = requests.post(config.url + 'channels/create/v2',
                            json={'token': token_2, 'name': 'channel_2',
                                    'is_public': False})
    channel_2_data = create_channel_2.json()
    channel_id_2 = channel_2_data['channel_id'] 

    # global owner join channel 2
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_1,
                        'channel_id': channel_id_2})

    # user 2 sends a message in channel 2
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 'channel_id': channel_id_2, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # global owner(user1) is able to message upon joinging the channel
    # (has owner permission if is a member)
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_1, 'message_id': message_id_2})
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_remove_global_user_fail(\
    clear_register_two_createchanneldm_sendmsg):
    """ testing if global owner cannot remove message if not in that channel """
    
    # user 1 is global owner
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # user2 creates private channel 2 and becomes owner of that channel
    create_channel_2 = requests.post(config.url + 'channels/create/v2',
                            json={'token': token_2, 'name': 'channel_2',
                                    'is_public': False})
    channel_2_data = create_channel_2.json()
    channel_id_2 = channel_2_data['channel_id'] 

    # user 2 sends a message in channel 2
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 'channel_id': channel_id_2, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # global owner(user1) cannot delete a message if not in channel
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_1, 'message_id': message_id_2})
    assert resp.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_sent_not_belong_to_user(clear_register_two_createchanneldm_sendmsg):
    """ testing if message cannot be removed by different user """

    channel_id = clear_register_two_createchanneldm_sendmsg[2]
    message_id = clear_register_two_createchanneldm_sendmsg[3]
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # user 2 joins channel 1 
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_2,
                        'channel_id': channel_id})

    # raise access error if user2 is trying to remove user1's message
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_2, 'message_id': message_id})
    assert resp.status_code == STATUS_ACCESS_ERR # raise access error

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_successful_message_remove_by_owner(\
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by channel owner """
    
    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    channel_id = clear_register_two_createchanneldm_sendmsg[2]
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # user 2 joins the channel 1
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_2,
                        'channel_id': channel_id})

    # user 2 sends a message in the channel 
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 'channel_id': channel_id, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # successful removal when user 1 who is the owner 
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': message_id_2})
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_successful_message_remove_by_user(clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by user who sent the message 
    """
    
    channel_id = clear_register_two_createchanneldm_sendmsg[2]
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # user 2 joins the channel 1
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_2,
                        'channel_id': channel_id})

    # user 2 sends a message in the channel 
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 'channel_id': channel_id, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # successful removal when user 2 tries to remove own message
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_2, 'message_id': message_id_2})
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_dm_successful_message_remove_by_user(clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by user who sent the message 
    """
    
    message_id =  clear_register_two_createchanneldm_sendmsg[5]
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # successful removal when user 2 tries to remove own message in dm
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_2, 'message_id': message_id})
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_dm_successful_message_remove_by_owner(clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by owner
    """
    
    message_id =  clear_register_two_createchanneldm_sendmsg[3]
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']

    # successful removal when user 1 who is owner of dm tries to remove message in dm
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_1, 'message_id': message_id})
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_dm_fail_message_remove(clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing fails if user does not have access
    """
    
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    dm_id = clear_register_two_createchanneldm_sendmsg[3]

    # create user 3
    user3 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'iii@def.com', 'password': 'password',
                        'name_first': 'first3', 'name_last': 'last3'})
    assert user3.status_code == STATUS_OK
    user_3 = user3.json()

    # user 1 sends message in dm
    send_message = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token_1,
                                'dm_id': dm_id, 
                                'message': 'hewwooooo'})
    assert send_message.status_code == STATUS_OK
    dm_message = send_message.json()
    message_id = dm_message['message_id']

    # raise access error when user 2 tries to remove user 1's message
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json={'token': token_2, 'message_id': message_id})
    assert resp.status_code == STATUS_ACCESS_ERR

    # access error when user3 tries to remove the message
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json={'token': user_3['token'],
                                'message_id': message_id})
    assert resp.status_code == STATUS_ACCESS_ERR
