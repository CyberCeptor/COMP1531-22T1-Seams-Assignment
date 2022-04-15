"""
Filename: message_sendlaterdm_test.py

Author: Yangjun Yue, z5317840
Created: 15/04/22

Description: pytests for
    - sending message to a specified channel at later time
"""

import pytest

import requests
from src import config
from src.other import cast_to_int_get_requests
import time
 
from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

time_later = 1
time_now = cast_to_int_get_requests(time.time(), 'time_sent needs to be int')
time_sent = time_now + time_later
past_time = time_now - time_later

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_token(clear_register_two_createdm):
    """ test for invalid input of token """

    # token is int
    dm_id = clear_register_two_createdm[2]
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
    """ test for invalid input of channel id """

    token = clear_register_two_createdm[0]['token']
    # no channel id input
    resp0 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': '', 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp0.status_code == STATUS_INPUT_ERR
    # channel id is boo
    resp1 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': True, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp1.status_code == STATUS_INPUT_ERR
    # channel id is string
    resp2 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': 'str', 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp2.status_code == STATUS_INPUT_ERR
    # wrong channel input
    resp3 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json = {'token': token, 'dm_id': 2, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_message_sendlater_invalid_message(clear_register_two_createdm):
    """ test for invalid input of message"""

    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]

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

    # time_sent is time in the past
    resp4 = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': past_time})
 
    assert resp4.status_code == STATUS_INPUT_ERR


@pytest.mark.usefixtures('clear_register_two_createdm')
def test_user_not_belong(clear_register_two_createdm):
    """ testing if user belongs to the channel """
    
    dm_id = clear_register_two_createdm[1]

    # create user 3
    user3 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'idk@abc.com', 
                            'password': 'password',
                            'name_first': 'first3', 'name_last': 'last3'}) 
    user3_data = user3.json()
    token_3 = user3_data['token']

    # access error when user 2 tries to send message in channel 1
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

    resp = requests.post(config.url + 'message/sendlaterdm/v1', 
                          json={'token': token, 'dm_id': dm_id, 
                          'message': 'hewwo', 'time_sent': time_sent})
 
    assert resp.status_code == STATUS_OK

    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': 0})
    assert resp1.status_code == 200
    info = resp1.json()
    assert(len(info['messages']) == 0)
    
    time.sleep(1)
    
    resp2 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': 0})
    assert resp2.status_code == 200
    info_later = resp1.json()
    assert(len(info_later['messages']) == 1)
    assert info_later['messages'][0]['message'] == 'hewwo'