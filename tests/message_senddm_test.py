"""
Filename: message_senddm_test.py

Author: Yangjun Yue, z5317840
Created: 25/03/22

Description: pytests for
    - sending message to a specified channel
"""

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_send_invalid_token(clear_register_two_createdm):
    """ test for invalid input of token """

    # token is int
    dm_id =  clear_register_two_createdm[2]
    resp0 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': 0, 'dm_id': dm_id, 
                          'message': 'hewwo'})
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is boo
    resp1 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': True, 'dm_id': dm_id, 
                          'message': 'hewwo'})
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': '', 'dm_id': dm_id, 
                          'message': 'hewwo'})
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': 'not right string', 
                          'dm_id': dm_id, 'message': 'hewwo'})
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': EXPIRED_TOKEN, 
                          'dm_id': dm_id, 'message': 'hewwo'})
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': UNSAVED_TOKEN, 
                          'dm_id': dm_id, 'message': 'hewwo'})
    assert resp5.status_code == STATUS_ACCESS_ERR
    
@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_send_invalid_channel_id(clear_register_two_createdm):
    """ test for invalid input of channel id """

    token =  clear_register_two_createdm[0]['token']
    # no dm id input
    resp0 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token, 'dm_id': '', 
                          'message': 'hewwo'})
    assert resp0.status_code == STATUS_INPUT_ERR
    # dm id is boo
    resp1 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token, 'dm_id': True, 
                          'message': 'hewwo'})
    assert resp1.status_code == STATUS_INPUT_ERR
    # dm id is string
    resp2 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token, 'dm_id': 'str', 
                          'message': 'hewwo'})
    assert resp2.status_code == STATUS_INPUT_ERR
    # invalid dm input
    resp3 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token, 'dm_id': 2, 
                          'message': 'hewwo'})
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_send_invalid_message(clear_register_two_createdm):
    """ test for invalid input of message """

    token =  clear_register_two_createdm[0]['token']
    dm_id =  clear_register_two_createdm[2]
    # message is int
    resp0 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token, 'dm_id': dm_id, 
                          'message': 0})
    assert resp0.status_code == STATUS_INPUT_ERR

    # message is boo
    resp1 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token, 'dm_id': dm_id, 
                          'message': True})
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_send_invalid_length(clear_register_two_createdm):
    """ test if input message length is valid(less than 1, over 1000 char) """

    token =  clear_register_two_createdm[0]['token']
    dm_id =  clear_register_two_createdm[2]
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
    resp0 = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': ''})
    assert resp0.status_code == STATUS_INPUT_ERR
    # more than 1000 character
    resp1 = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': long_message})
    assert resp1.status_code == STATUS_INPUT_ERR
   
@pytest.mark.usefixtures('clear_register_two_createdm')
def test_user_not_belong(clear_register_two_createdm):
    """ testing if user belongs to the channel """
    
    dm_id =  clear_register_two_createdm[2]

    # create user 3
    user3 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'hij@abc.com', 
                            'password': 'password',
                            'name_first': 'first3', 'name_last': 'last3'}) 
    user3_data = user3.json()
    token_3 = user3_data['token']

    # user 3 tries to send message in dm1
    resp0 = requests.post(config.url + 'message/senddm/v1', 
                          json = {'token': token_3, 'dm_id': dm_id, 
                          'message': 'hewwofrom3'})
    assert resp0.status_code == STATUS_ACCESS_ERR #raise access error

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_successful_message_send(clear_register_two_createdm):
    """ testing gor successful run of message send v1 and return """
    
    token =  clear_register_two_createdm[1]['token']
    dm_id =  clear_register_two_createdm[2]

    send_message = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo'})
    assert send_message.status_code == STATUS_OK
    
    message = send_message.json()
    message_id = message['message_id']
    assert message_id == 1
    # send another message
    send_message_2 = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwoagain'})
    assert send_message_2.status_code == STATUS_OK
    message = send_message_2.json()
    message_id = message['message_id']
    assert message_id == 2
    
requests.delete(config.url + 'clear/v1')
