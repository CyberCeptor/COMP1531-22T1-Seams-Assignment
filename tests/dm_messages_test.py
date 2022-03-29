"""
Filename: dm_messages_test.py

Author: Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: pytests for dm_messages_v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_messages_invalid_dm(clear_register_two_createdm):
    """ testing invalid dm id to raise input error """

    token = clear_register_two_createdm[0]['token']
   
    # no dm id input
    resp0 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': '', 'start': 0})
    assert resp0.status_code == 400
    # dm id is boo
    resp1 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': True, 'start': 0})
    assert resp1.status_code == 400
    # dm id is string
    resp2 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': 'not int', 
                                    'start': 0})
    assert resp2.status_code == 400
    # wrong dm input
    resp3 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': 5, 'start': 0})
    assert resp3.status_code == 400
    resp4 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': -1, 'start': 0})
    assert resp4.status_code == 400

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_messages_invalid_token(clear_register_two_createdm):
    """ testing invalid input of token """

    dm_id = clear_register_two_createdm[2]
   
    # no token input
    resp0 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': '', 'dm_id': dm_id, 'start': 0})
    assert resp0.status_code == 400

    # token is boo
    resp1 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': True, 'dm_id': dm_id, 'start': 0})
    assert resp1.status_code == 400

    resp2 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': False, 'dm_id': dm_id, 'start': 0})
    assert resp2.status_code == 400

    # wrong token input
    resp3 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': 'str', 'dm_id': dm_id, 'start': 0})
    # wrong token type int                      
    assert resp3.status_code == 403
    resp4 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': 0, 'dm_id': dm_id, 'start': 0})
    assert resp4.status_code == 400

    # expired token
    resp5 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': expired_token, 'dm_id': dm_id, 
                                    'start': 0})
    assert resp5.status_code == 403

    # unsaved token
    resp6 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': unsaved_token, 'dm_id': dm_id, 
                                    'start': 0})
    assert resp6.status_code == 403
    
    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_dm_messages_invalid_start(clear_register_two_createdm):
    """ testing if start is int """

    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]
    # start is bool
    resp0 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': True})
    assert resp0.status_code == 400
    resp1 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': False})
    assert resp1.status_code == 400
    # start is str
    resp2 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': ''})
    assert resp2.status_code == 400
    resp3 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': 'str'})
    assert resp3.status_code == 400
    # start is too big or negative
    resp4 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': -5})
    assert resp4.status_code == 400
    resp5 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 
                                    'start': 1000})
    assert resp5.status_code == 400

@pytest.mark.usefixtures('clear_register_two_createdm')
def test_user_not_belong(clear_register_two_createdm):
    """ testing if user belongs to the dm """
    
    dm_id = clear_register_two_createdm[2]

    # create user 2
    user2 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_data = user2.json()
    token_2 = user2_data['token']

    resp0 = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token_2, 'dm_id': dm_id, 
                                    'start': True})
    assert resp0.status_code == 403

@pytest.mark.usefixtures('clear_register_two_createdm')   
def test_dm_messages_return(clear_register_two_createdm):
    """ testing dm_message returns empty if no message """

    token = clear_register_two_createdm[0]['token']
    dm_id = clear_register_two_createdm[2]

    # test success run
    resp = requests.get(config.url + 'dm/messages/v1', 
                          params = {'token': token, 'dm_id': dm_id, 'start': 0})
    assert resp.status_code == 200
    dm_messages = resp.json()

    assert dm_messages['messages'] == []
    assert dm_messages['start'] == 0
    assert dm_messages['end'] == -1
