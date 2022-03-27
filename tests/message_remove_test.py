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

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_message_remove_invalid_token(clear_register_createchannel_sendmsg):
    """ test for invalid input of token """

    # token is int
    message_id = clear_register_createchannel_sendmsg[2]
    resp0 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': 0, 'message_id': message_id})
    assert resp0.status_code == 400

    # token is boo
    resp1 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': True, 'message_id': message_id})
    assert resp1.status_code == 400

    # token input empty
    resp2 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': '', 'message_id': message_id})
    assert resp2.status_code == 400

    # wrong token input
    resp3 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': 'str', 'message_id': message_id})
    assert resp3.status_code == 403

    # expired token
    resp4 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': expired_token, 
                          'message_id': message_id})
    assert resp4.status_code == 403

    # unsaved token
    resp5 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': unsaved_token, 
                          'message_id': message_id})
    assert resp5.status_code == 403
    
@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_message_remove_invalid_message_id(\
    clear_register_createchannel_sendmsg):
    """ test for invalid input of channel id """

    token = clear_register_createchannel_sendmsg[0]
    # no message id input
    resp0 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': ''})
    assert resp0.status_code == 400
    # message id is boo
    resp1 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': True})
    assert resp1.status_code == 400
    # message id is string
    resp2 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': 'str'})
    assert resp2.status_code == 400
    # non-existent message id
    resp3 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': -1})
    assert resp3.status_code == 400
    resp4 = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token, 'message_id': 100})
    assert resp4.status_code == 400


@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_message_remove_global_user(clear_register_createchannel_sendmsg):
    """ testing if global owner cannot remove message if not in that channel """
    
    token = clear_register_createchannel_sendmsg[0] # user 1 is global owner
    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 
                            'password': 'password',
                            'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

    # user2 creates private channel 2 and becomes owner of that channel
    create_channel_2 = requests.post(config.url + 'channels/create/v2',
                            json={'token': token_2, 'name': 'channel_2',
                                    'is_public': False})
    channel_2_data = create_channel_2.json()
    channel_id_2 = channel_2_data['channel_id'] 

    # global owner join channel 2
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token,
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
                          json = {'token': token, 'message_id': message_id_2})
    assert resp.status_code == 200

@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_message_remove_global_user_fail(\
    clear_register_createchannel_sendmsg):
    """ testing if global owner cannot remove message if not in that channel """
    
    token = clear_register_createchannel_sendmsg[0] # user 1 is global owner
    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 
                            'password': 'password',
                            'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

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
                          json = {'token': token, 'message_id': message_id_2})
    assert resp.status_code == 403

@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_message_sent_not_belong_to_user(clear_register_createchannel_sendmsg):
    """ testing if message cannot be removed by different user """

    channel_id = clear_register_createchannel_sendmsg[1]
    message_id = clear_register_createchannel_sendmsg[2]

    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 
                            'password': 'password',
                            'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

    # user 2 joins channel 1 
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_2,
                        'channel_id': channel_id})

    # raise access error if user2 is trying to remove user1's message
    resp = requests.delete(config.url + 'message/remove/v1', 
                          json = {'token': token_2, 'message_id': message_id})
    assert resp.status_code == 403 # raise access error

@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_successful_message_remove_by_owner(\
    clear_register_createchannel_sendmsg):
    """ testing if message removing is successful by channel owner """
    
    token = clear_register_createchannel_sendmsg[0]
    channel_id = clear_register_createchannel_sendmsg[1]

    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

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
    assert resp.status_code == 200

@pytest.mark.usefixtures('clear_register_createchannel_sendmsg')
def test_successful_message_remove_by_user(clear_register_createchannel_sendmsg):
    """ testing if message removing is successful by user who sent the message 
    """
    
    channel_id = clear_register_createchannel_sendmsg[1]
    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

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
    assert resp.status_code == 200

requests.delete(config.url + 'clear/v1')
