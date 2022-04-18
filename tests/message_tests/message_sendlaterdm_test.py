"""
Filename: message_sendlaterdm_test.py

Author: Yangjun Yue, z5317840
Created: 15/04/22

Description: pytests for
    - sending message to a specified dm at later time
"""

import time

import pytest

import requests

from src import config
 
from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

TIME_LATER = 1
TWO_TIME_LATER = 2

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_token(clear_register_two_createdm):
    """ test for invalid input of token """

    dm_id = clear_register_two_createdm[2]

    time_sent = int(time.time()) + TIME_LATER

    # token is int
    resp0 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': 0, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is boo
    resp1 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': True, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': '', 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': 'not right string', 
                          'dm_id': dm_id, 'message': 'hewwo',
                          'time_sent':time_sent})
 
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': EXPIRED_TOKEN, 
                          'dm_id': dm_id, 'message': 'hewwo',
                          'time_sent': time_sent})
 
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': UNSAVED_TOKEN, 
                          'dm_id': dm_id, 'message': 'hewwo', 
                          'time_sent': time_sent})
 
    assert resp5.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_dm_id(clear_register_two_createdm):
    """ test for invalid input of dm id """

    token = clear_register_two_createdm[0]['token']

    time_sent = int(time.time()) + TIME_LATER

    # no dm id input
    resp0 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': '', 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp0.status_code == STATUS_INPUT_ERR
    # dm id is boo
    resp1 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': True, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp1.status_code == STATUS_INPUT_ERR
    # dm id is string
    resp2 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': 'str', 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp2.status_code == STATUS_INPUT_ERR
    # wrong dm input
    resp3 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': 2, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_message(clear_register_two_createdm):
    """ test for invalid input of message"""

    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]

    time_sent = int(time.time()) + TIME_LATER

    # message is int
    resp0 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': dm_id, 
                          'message': 0, 'time_sent': time_sent})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # message is boo
    resp1 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': dm_id, 
                          'message': True, 'time_sent': time_sent})
 
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_length(clear_register_two_createdm):
    """ test if input message length is valid(less than 1, over 1000 char) """

    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]

    time_sent = int(time.time()) + TIME_LATER

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
    resp0 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': '', 'time_sent': time_sent})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # more than 1000 character
    resp1 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': long_message, 'time_sent': time_sent})
 
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_time_sent(clear_register_two_createdm):
    """ test for invalid input of message"""

    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]

    # time_sent is wrong int
    resp1 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': 0})
 
    assert resp1.status_code == STATUS_INPUT_ERR

    # time_sent is str
    resp2 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': 'str'})
 
    assert resp2.status_code == STATUS_INPUT_ERR

    # time_sent is bool
    resp3 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': True})
 
    assert resp3.status_code == STATUS_INPUT_ERR

    past_time = int(time.time()) - TIME_LATER

    # time_sent is time in the past
    resp4 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': past_time})
 
    assert resp4.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_user_not_belong(clear_register_two_createdm):
    """ testing if user belongs to the dm """
    
    dm_id = clear_register_two_createdm[2]

    time_sent = int(time.time()) + TIME_LATER

    # create user 3
    user3 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'idk@abc.com', 
                            'password': 'password',
                            'name_first': 'first3', 'name_last': 'last3'}) 
    user3_data = user3.json()
    token_3 = user3_data['token']

    # access error when user 2 tries to send message in dm 1
    # raise access error 
    resp0 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token_3, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp0.status_code == STATUS_ACCESS_ERR 

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_successful_message_sendlater(clear_register_two_createdm):
    """ testing gor successful run of message send v1 and return """
    
    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]

    time_sent = int(time.time()) + TIME_LATER

    resp = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp.status_code == STATUS_OK

    resp1 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': 0})
    assert resp1.status_code == 200
    info = resp1.json()
    assert(len(info['messages']) == 0)
    
    time.sleep(TWO_TIME_LATER)
    
    resp2 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': 0})
    assert resp2.status_code == 200
    info_later = resp2.json()
    assert(len(info_later['messages']) == 1)
    assert info_later['messages'][0]['message'] == 'hewwo'

requests.delete(config.url + 'clear/v1')
