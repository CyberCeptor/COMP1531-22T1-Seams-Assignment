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

@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    requests.delete(config.url + 'clear/v1')
    register = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data = register.json()
    token = user_data['token']

    create_channel = requests.post(config.url + 'channels/create/v2',
                            json={'token': token, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = create_channel.json()
    channel_id = channel_data['channel_id']                             

    return [token, channel_id]


def test_message_send_invalid_token(clear_and_register_and_create):
    """
    test for invalid input of token

    Arguments: clear_and_register_and_create

    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument

    # token is int
    chan_id = clear_and_register_and_create[1]
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': 0, 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp0.status_code == 400
    # token is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': True, 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp1.status_code == 400
    # token input empty
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': '', 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp2.status_code == 400
    # wrong token input
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': 'not right string', 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp3.status_code == 403
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    resp4 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': expired_token, 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp4.status_code == 403
    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSw\
            iaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRq\
            pQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    resp5 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': unsaved_token, 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp5.status_code == 403
    
    requests.delete(config.url + 'clear/v1')

def test_message_send_invalid_channel_id(clear_and_register_and_create):
    """
    test for invalid input of channel id

    Arguments: clear_and_register_and_create

    Exceptions: N/A

    Return Value: N/A
    """

    token = clear_and_register_and_create[0]
    # no channel id input
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': '', 'message': 'hewwo'})
    assert resp0.status_code == 400
    # channel id is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': True, 'message': 'hewwo'})
    assert resp1.status_code == 400
    # channel id is string
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': 'str', 'message': 'hewwo'})
    assert resp2.status_code == 400
    # wrong channel input
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': 2, 'message': 'hewwo'})
    assert resp3.status_code == 400

    requests.delete(config.url + 'clear/v1')

def test_message_send_invalid_message(clear_and_register_and_create):
    """
    test for invalid input of message

    Arguments: clear_and_register_and_create

    Exceptions: N/A

    Return Value: N/A
    """

    token = clear_and_register_and_create[0]
    chan_id = clear_and_register_and_create[1]
    # message is int
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': chan_id, 'message': 0})
    assert resp0.status_code == 400

    # message is boo
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token, 'channel_id': chan_id, 'message': True})
    assert resp1.status_code == 400

    requests.delete(config.url + 'clear/v1')

def test_message_send_invalid_length(clear_and_register_and_create):
    """
    test if input message length is valid(less than 1, over 1000 char)

    Arguments:  clear_and_register_and_create

    Exceptions:
        InputError  -   Raised for all tests below

    Return Value:   N/A
    """

    token = clear_and_register_and_create[0]
    chan_id = clear_and_register_and_create[1]
    # long_message is more than 1000 char
    long_message = 'MoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanAt\
    housandCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMo\
    reThanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousandChara\
    ctersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousan\
    dCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanA\
    thousandCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMo\
    reThanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousandCharac\
    tersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousand\
    CharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanAtho\
    usandCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreThanA\
    thousandCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMoreT\
    hanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousandCharactersMo\
    reThanAthousandCharactersMoreThanAthousandCharactersMoreThanAthousandCharacters\
    MoreThanAthousandCharactersMoreThanAthousandCharacters'

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

def test_user_not_belong(clear_and_register_and_create):
    """
    testing if user belongs to the channel

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: 
        Access Error - Raised for all test cases below

    Return Value: N/A
    """
    
    chan_id = clear_and_register_and_create[1]

    # create user 2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']

    resp0 = requests.post(config.url + 'message/send/v1', 
                          json = {'token': token_2, 'channel_id': chan_id, 'message': 'hewwo'})
    assert resp0.status_code == 403 #raise access error

    requests.delete(config.url + 'clear/v1')

def test_successful_message_send(clear_and_register_and_create):
    """
    testing gor successful run of message send v1 and return

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    
    token = clear_and_register_and_create[0]
    chan_id = clear_and_register_and_create[1]

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

