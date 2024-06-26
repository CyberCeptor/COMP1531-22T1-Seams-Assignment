"""
Filename: message_send_test.py

Author: Yangjun Yue, z5317840
Created: 23/03/22

Description: pytests for
    - sending message to a specified channel
"""

import pytest

import requests
from src import config

 
from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_token(clear_register_createchannel):
    """ test for invalid input of token """

    # token is int
    chan_id = clear_register_createchannel[1]
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': 0, 'channel_id': chan_id, 
                          'message': 'hewwo'})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': True, 'channel_id': chan_id, 
                          'message': 'hewwo'})
 
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': '', 'channel_id': chan_id, 
                          'message': 'hewwo'})
 
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': 'not right string', 
                          'channel_id': chan_id, 'message': 'hewwo'})
 
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': EXPIRED_TOKEN, 
                          'channel_id': chan_id, 'message': 'hewwo'})
 
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': UNSAVED_TOKEN, 
                          'channel_id': chan_id, 'message': 'hewwo'})
 
    assert resp5.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_channel_id(clear_register_createchannel):
    """ test for invalid input of channel id """

    token = clear_register_createchannel[0]['token']
    # no channel id input
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': '', 
                          'message': 'hewwo'})
 
    assert resp0.status_code == STATUS_INPUT_ERR
    # channel id is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': True, 
                          'message': 'hewwo'})
 
    assert resp1.status_code == STATUS_INPUT_ERR
    # channel id is string
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': 'str', 
                          'message': 'hewwo'})
 
    assert resp2.status_code == STATUS_INPUT_ERR
    # wrong channel input
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': 2, 
                          'message': 'hewwo'})
 
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_message(clear_register_createchannel):
    """ test for invalid input of message"""

    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    # message is int
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': chan_id, 
                          'message': 0})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # message is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': chan_id, 
                          'message': True})
 
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_length(clear_register_createchannel):
    """ test if input message length is valid(less than 1, over 1000 char) """

    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]
    # long_message is more than 1000 char
    long_message = 'MoreThanAthousandCharactersMoreThanAthousandCharactersMor\
        eThanAt housandCharactersMoreThanAthousandCharactersMoreThanAthousand\
        CharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreT\
        hanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousandCha\
        ractersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThan\
        AthousandCharactersMoreThanAthousandCharactersMoreThanAthousandCharac\
        tersMoreThanAthousandCharactersMo reThanAthousandCharactersMoreThanAt\
        housandCharactersMoreThanAthousandCharactersMoreThanAthousandCharacte\
        rsMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanAthou\
        sandCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersM\
        oreThanAthousandCharactersMoreThanAthousandCharactersMoreThanA thousa\
        ndCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMor\
        eT hanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousand\
        CharactersMo reThanAthousandCharactersMoreThanAthousandCharactersMore\
        ThanAthousandCharacters MoreThanAthousandCharactersMoreThanAthousandC\
        haracters'

    # less than 1 character
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id, 
                          'message': ''})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # more than 1000 character
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id, 
                          'message': long_message})
 
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_user_not_belong(clear_register_createchannel):
    """ testing if user belongs to the channel """
    
    chan_id = clear_register_createchannel[1]

    # create user 2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 
                            'password': 'password',
                            'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']
    # access error when user 2 tries to send message in channel 1
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token_2, 'channel_id': chan_id, 
                          'message': 'hewwo'})
 
    assert resp0.status_code == STATUS_ACCESS_ERR #raise access error

@pytest.mark.usefixtures('clear_register_createchannel')
def test_successful_message_send(clear_register_createchannel):
    """ testing gor successful run of message send v1 and return """
    
    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id, 
                          'message': 'hewwo'})
 
    assert send_message.status_code == STATUS_OK
    message = send_message.json()
    message_id = message['message_id']
    assert message_id == 1

    # create a second channel to send message
    create_2_channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': token, 'name': 'channel_2',
                                    'is_public': True})
 
    assert create_2_channel.status_code == STATUS_OK                               
    channel_2_data = create_2_channel.json()
    channel_2_id = channel_2_data['channel_id']
    
    # send second message in a different channel
    send_2_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_2_id, 
                          'message': 'hewwoagain'})
 
    assert send_2_message.status_code == STATUS_OK
    message2 = send_2_message.json()
    message_2_id = message2['message_id']
    assert message_2_id == 2
  
requests.delete(config.url + 'clear/v1')
