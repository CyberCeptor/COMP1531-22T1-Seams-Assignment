"""
Filename: message_edit_test.py

Author: Yangjun Yue, z5317840
Created: 23/03/22

Description: pytests for
    - editing message given a message id
"""

import pytest

import requests

from src import config

@pytest.fixture(name='create_message')
def fixture_create_message():
    """
    clears any data stored in data_store and registers a user with the
    given information, create a channel using user id, send a message to channel

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

    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token, 'channel_id': channel_id, 
                          'message': 'hewwo'})
    message = send_message.json()
    message_id = message['message_id']
 
    return [token, channel_id, message_id]


def test_message_edit_invalid_token(create_message):
    """
    test for invalid input of token

    Arguments: create_message
    Exceptions: N/A

    Return Value: N/A
    """
    # pylint: disable=unused-argument

    # token is int
    message_id = create_message[2]
    resp0 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': 0, 'message_id': message_id, 'message': 'hewwo'})
    assert resp0.status_code == 400
    # token is boo
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': True, 'message_id': message_id, 'message': 'hewwo'})
    assert resp1.status_code == 400
    # token input empty
    resp2 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': '', 'message_id': message_id, 'message': 'hewwo'})
    assert resp2.status_code == 400
    # wrong token input
    resp3 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': 'str', 'message_id': message_id, 'message': 'hewwo'})
    assert resp3.status_code == 400
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    resp4 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': expired_token, 'message_id': message_id, 'message': 'hewwo'})
    assert resp4.status_code == 403
    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSw\
            iaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRq\
            pQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    resp5 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': unsaved_token, 'message_id': message_id, 'message': 'hewwo'})
    assert resp5.status_code == 403
    
    requests.delete(config.url + 'clear/v1')

def test_message_edit_invalid_message_id(create_message):
    """
    test for invalid input of channel id

    Arguments: create_message

    Exceptions: N/A

    Return Value: N/A
    """

    token = create_message[0]
    # no message id input
    resp0 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': '', 'message': 'hewwo'})
    assert resp0.status_code == 400
    # message id is boo
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': True, 'message': 'hewwo'})
    assert resp1.status_code == 400
    # message id is string
    resp2 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': 'str', 'message': 'hewwo'})
    assert resp2.status_code == 400
    # non-existent message id
    resp3 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': -1, 'message': 'hewwo'})
    assert resp3.status_code == 400
    resp4 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': 100, 'message': 'hewwo'})
    assert resp4.status_code == 400

    requests.delete(config.url + 'clear/v1')


def test_message_edit_invalid_message(create_message):
    """
    test for invalid input of message

    Arguments: create_message

    Exceptions: N/A

    Return Value: N/A
    """

    token = create_message[0]
    message_id = create_message[2]
    # message is int
    resp0 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': message_id, 'message': 0})
    assert resp0.status_code == 400

    # message is boo
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': message_id, 'message': True})
    assert resp1.status_code == 400

    requests.delete(config.url + 'clear/v1')

def test_message_send_invalid_length(create_message):
    """
    test if input message length is valid(less than 1, over 1000 char)

    Arguments:  create_message

    Exceptions:
        InputError  -   Raised for all tests below

    Return Value:   N/A
    """

    token = create_message[0]
    message_id = create_message[2]

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

    # more than 1000 character
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': message_id, 
                          'message': long_message})
    assert resp1.status_code == 400

    requests.delete(config.url + 'clear/v1')

def test_message_not_belong_to_channel(create_message):
    """
    testing if message belongs to the channel

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: 
        Input Error - Raised for all test cases below

    Return Value: N/A
    """
    
    token = create_message[0]
    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

    # user2 creates private channel 2
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

    # message_id does not refer to a valid message within a 
    # channel/DM that the authorised user has joined
    resp = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': message_id_2, 'message': 'attempt'})
    assert resp.status_code == 400 

    requests.delete(config.url + 'clear/v1')


def test_message_sent_not_belong_to_user(create_message):
    """
    testing if message is sent by the user who makes the editing request

    Arguments: create_message(fixture)

    Exceptions: 
        Access Error - Raised for all test cases below

    Return Value: N/A
    """
    channel_id = create_message[1]
    message_id = create_message[2]
    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

    # user 2 joins channel 1 but did not send the message
    requests.post(config.url + 'channel/join/v2',
                        json = {'token': token_2,
                        'channel_id': channel_id})

    # raise access error if user2 is trying to edit user1's message
    resp = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token_2, 'message_id': message_id, 'message': 'attempt'})
    assert resp.status_code == 403 # raise access error

    requests.delete(config.url + 'clear/v1')

def test_successful_message_edit(create_message):
    """
    testing if message editing is successful

    Arguments: create_message(fixture)

    Exceptions: 
        Access Error - Raised for all test cases below

    Return Value: N/A
    """
    
#         the authorised user has owner permissions in the channel/DM

    token = create_message[0]
    channel_id = create_message[1]
    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()
    token_2 = user2_json['token']

    # user 2 sends a message in the channel 
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 'channel_id': channel_id, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # successful edit when user 1 who is the owner edits user2's message
    resp = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': message_id_2, 'message': 'attempt'})
    assert resp.status_code == 200

    # successful edit when user 2 tries to edit user2's message
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token_2, 'message_id': message_id_2, 'message': 'attempt'})
    assert resp1.status_code == 200
    requests.delete(config.url + 'clear/v1')

def test_message_edit_empty(create_message):
    """
    testing if entered message is empty, the message is deleted

    Arguments: create_message(fixture)

    Exceptions: N/A

    Return Value: N/A
    """

    token = create_message[0]
    message_id = create_message[2]
    resp = requests.put(config.url + 'message/edit/v1', 
                          json = {'token': token, 'message_id': message_id, 'message': ''})
    assert resp.status_code == 200