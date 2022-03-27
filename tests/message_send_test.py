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


@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_token(clear_register_createchannel):
    """
    test for invalid input of token

    Arguments: clear_register_createchannel

    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument

    # token is int
    chan_id = clear_register_createchannel[1]
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': 0, 'channel_id': chan_id, 
                          'message': 'hewwo'})
    assert resp0.status_code == 400
    # token is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': True, 'channel_id': chan_id, 
                          'message': 'hewwo'})
    assert resp1.status_code == 400
    # token input empty
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': '', 'channel_id': chan_id, 
                          'message': 'hewwo'})
    assert resp2.status_code == 400
    # wrong token input
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': 'not right string', 
                          'channel_id': chan_id, 'message': 'hewwo'})
    assert resp3.status_code == 403
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    resp4 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': expired_token, 
                          'channel_id': chan_id, 'message': 'hewwo'})
    assert resp4.status_code == 403
    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwi\
        c2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc\
        3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    resp5 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': unsaved_token, 
                          'channel_id': chan_id, 'message': 'hewwo'})
    assert resp5.status_code == 403
    
    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_channel_id(clear_register_createchannel):
    """
    test for invalid input of channel id

    Arguments: clear_register_createchannel

    Exceptions: N/A

    Return Value: N/A
    """

    token = clear_register_createchannel[0]['token']
    # no channel id input
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': '', 
                          'message': 'hewwo'})
    assert resp0.status_code == 400
    # channel id is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': True, 
                          'message': 'hewwo'})
    assert resp1.status_code == 400
    # channel id is string
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': 'str', 
                          'message': 'hewwo'})
    assert resp2.status_code == 400
    # wrong channel input
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': 2, 
                          'message': 'hewwo'})
    assert resp3.status_code == 400

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_message(clear_register_createchannel):
    """
    test for invalid input of message

    Arguments: clear_register_createchannel

    Exceptions: N/A

    Return Value: N/A
    """

    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]
    # message is int
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': chan_id, 
                          'message': 0})
    assert resp0.status_code == 400

    # message is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': chan_id, 
                          'message': True})
    assert resp1.status_code == 400

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_message_send_invalid_length(clear_register_createchannel):
    """
    test if input message length is valid(less than 1, over 1000 char)

    Arguments:  clear_register_createchannel

    Exceptions:
        InputError  -   Raised for all tests below

    Return Value:   N/A
    """

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
    assert resp0.status_code == 400
    # more than 1000 character
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id, 
                          'message': long_message})
    assert resp1.status_code == 400

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
                            json={'email': 'def@abc.com', 
                            'password': 'password',
                            'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']
    # access error when user 2 tries to send message in channel 1
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token_2, 'channel_id': chan_id, 
                          'message': 'hewwo'})
    assert resp0.status_code == 403 #raise access error

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_createchannel')
def test_successful_message_send(clear_register_createchannel):
    """
    testing gor successful run of message send v1 and return

    Arguments: clear_register_createchannel (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    
    token = clear_register_createchannel[0]['token']
    chan_id = clear_register_createchannel[1]

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': chan_id, 
                          'message': 'hewwo'})
    assert send_message.status_code == 200
    
    message = send_message.json()
    message_id = message['message_id']
    assert message_id == 1
    # create a second channel to send message
    create_2_channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': token, 'name': 'channel_2',
                                    'is_public': True})
    assert create_2_channel.status_code == 200                               
    channel_2_data = create_2_channel.json()
    channel_2_id = channel_2_data['channel_id']
    # send second message in a different channel
    send_2_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_2_id, 
                          'message': 'hewwoagain'})
    assert send_2_message.status_code == 200
    message2 = send_2_message.json()
    message_2_id = message2['message_id']
    assert message_2_id == 2
    
    requests.delete(config.url + 'clear/v1')

