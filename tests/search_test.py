"""
Filename: search_test.py

Author: Yangjun Yue, z5317840
Created: 07/03/22

Description: pytests for
    - searchnig correlated messages with a query string
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures()
def test_search_invalid_token():
    """ testing invalid user type to raise input error """

    # token is int
    resp0 = requests.get(config.url + 'search/v1', 
                          params={'token': 0, 'query_str': 'hewwo'})
    assert resp0.status_code == 400

    # token is boo
    resp1 = requests.get(config.url + 'search/v1', 
                          params={'token': True, 'query_str': 'hewwo'})
    assert resp1.status_code == 400

    # token input empty
    resp2 = requests.get(config.url + 'search/v1', 
                          params={'token': '', 'query_str': 'hewwo'})
    assert resp2.status_code == 400

    # wrong token input
    resp3 = requests.get(config.url + 'search/v1', 
                          params={'token': 'not right string',
                                  'query_str': 'hewwo'})
    assert resp3.status_code == 403

    # expired token
    resp4 = requests.get(config.url + 'search/v1', 
                         params={'token': expired_token, 'query_str': 'hewwo'})
    assert resp4.status_code == 403

    # unsaved token
    resp5 = requests.get(config.url + 'search/v1', 
                         params={'token': unsaved_token, 'query_str': 'hewwo'})
    assert resp5.status_code == 403

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_search_invalid_query_string(clear_register_two_createchanneldm_sendmsg):
    """ testing invalid query string to raise input error """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    # query string less than 1 char
    resp0 = requests.get(config.url + 'search/v1', 
                         params={'token': token, 'query_str': ''})
    assert resp0.status_code == 400

    # query string more than 1000 char
    long_str = 'MoreThanAthousandCharactersMoreThanAthousandCharactersMor\
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
    resp1 = requests.get(config.url + 'search/v1', 
                         params={'token': token, 'query_str': long_str})
    assert resp1.status_code == 400

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_search_successful(clear_register_two_createchanneldm_sendmsg):
    """ testing successful seach """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    user1_id = clear_register_two_createchanneldm_sendmsg[0]['auth_user_id']
    user2_id = clear_register_two_createchanneldm_sendmsg[1]['auth_user_id']
    c_message_id = clear_register_two_createchanneldm_sendmsg[3]
    d_message_id = clear_register_two_createchanneldm_sendmsg[5]
    resp0 = requests.get(config.url + 'search/v1', 
                         params={'token': token, 'query_str': 'hewwo'})
    assert resp0.status_code == 200

    searched_message = resp0.json()
    assert len(searched_message) == 2

    # check returned first message, 'hewwo' sent by user 1 in channel 1
    assert (c_message_id, user1_id) in [(k['message_id'],k['u_id']) 
                                        for k in searched_message]

    # check returned second message, 'hewwo' sent by user 2 in dm 1
    assert (d_message_id, user2_id) in [(k['message_id'],k['u_id']) 
                                        for k in searched_message]



@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_search_successful_user2(clear_register_two_createchanneldm_sendmsg):
    """ testing successful seach """

    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    user2_id = clear_register_two_createchanneldm_sendmsg[1]['auth_user_id']
    d_message_id = clear_register_two_createchanneldm_sendmsg[5]

    # user 2 queries hewwo, will only return dm message since user 2
    # is not in channel
    resp0 = requests.get(config.url + 'search/v1', 
                         params={'token': token_2, 'query_str': 'hewwo'})
    assert resp0.status_code == 200

    searched_message = resp0.json()
    assert len(searched_message) == 1

    assert (d_message_id, user2_id) in [(k['message_id'],k['u_id']) 
                                        for k in searched_message]

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_search_user_not_in_channel(clear_register_two_createchanneldm_sendmsg):
    """ testing successful search """

    # create user 3 not in channel or dm
    resp = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@hsh.com', 'password': 'password',
                                'name_first': 'first3', 'name_last': 'last3'})
    assert resp.status_code == 200
    user3 = resp.json()
    token_3 = user3['token']

    # would return empty list of messages
    resp0 = requests.get(config.url + 'search/v1', 
                         params={'token': token_3, 'query_str': 'hewwo'})
    assert resp0.status_code == 200
    msg_return = resp0.json()
    assert msg_return == []

requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_search_case_insensitive(clear_register_two_createchannel):
    """ testing successful seach """

    token = clear_register_two_createchannel[0]['token']
    user1_id = clear_register_two_createchannel[0]['auth_user_id']
    c_id = clear_register_two_createchannel[2]

    # user1 sends another message in channel 1
    # testing case insensitive and non letters
    resp = requests.post(config.url + 'message/send/v1', 
                          json={'token': token,
                                'channel_id': c_id, 
                                'message': 'HEWWOagain@@'})
    assert resp.status_code == 200
    chan_message = resp.json()
    msg_id = chan_message['message_id']

    resp0 = requests.get(config.url + 'search/v1', 
                         params={'token': token, 'query_str': 'hewwo'})
    assert resp0.status_code == 200
    searched_message = resp0.json()

    assert (msg_id, user1_id) in [(k['message_id'],k['u_id']) 
                                    for k in searched_message]


