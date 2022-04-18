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

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_edit_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of token """

    # token is int
    message_id = clear_register_two_createchanneldm_sendmsg[3]
    
    resp0 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': 0, 'message_id': message_id,
                                'message': 'hewwo'})
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is bool
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': True, 'message_id': message_id,
                                'message': 'hewwo'})
    assert resp1.status_code == STATUS_INPUT_ERR
    
    # token input empty
    resp2 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': '', 'message_id': message_id, 
                                'message': 'hewwo'})
 
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': 'str', 'message_id': message_id, 
                                'message': 'hewwo'})
 
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.put(config.url + 'message/edit/v1', 
                         json={'token': EXPIRED_TOKEN, 'message_id': message_id,
                               'message': 'hewwo'})
 
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.put(config.url + 'message/edit/v1', 
                         json={'token': UNSAVED_TOKEN, 'message_id': message_id,
                               'message': 'hewwo'})
 
    assert resp5.status_code == STATUS_ACCESS_ERR
    
@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_edit_invalid_message_id(
    clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of channel id """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']

    # no message id input
    resp0 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': '', 
                                'message': 'hewwo'})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # message id is bool
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': True,
                                'message': 'hewwo'})
 
    assert resp1.status_code == STATUS_INPUT_ERR

    # message id is string
    resp2 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': 'str', 
                                'message': 'hewwo'})
 
    assert resp2.status_code == STATUS_INPUT_ERR

    # non-existent message ids
    resp3 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': -1, 
                                'message': 'hewwo'})
 
    assert resp3.status_code == STATUS_INPUT_ERR

    resp4 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': 100, 
                                'message': 'hewwo'})
 
    assert resp4.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_edit_invalid_message(
    clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of message """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    message_id = clear_register_two_createchanneldm_sendmsg[3]

    # message is int
    resp0 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': message_id, 
                                'message': 0})
 
    assert resp0.status_code == STATUS_INPUT_ERR

    # message is bool
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': message_id, 
                                'message': True})
 
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_send_invalid_length(
    clear_register_two_createchanneldm_sendmsg):
    """ test if input message length is valid(less than 1, over 1000 char) """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    message_id = clear_register_two_createchanneldm_sendmsg[3]

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

    # more than 1000 character
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': message_id, 
                          'message': long_message})
 
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_edit_different_message(
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message belongs to the channel """
    
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

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
                          json={'token': token_1, 'message_id': message_id_2, 
                                'message': 'attempt'})
 
    assert resp.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_sent_not_belong_to_user(
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message is sent by the user who makes the editing request """

    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    channel_id = clear_register_two_createchanneldm_sendmsg[2]
    message_id = clear_register_two_createchanneldm_sendmsg[3]

    # user 2 joins channel 1 but did not send the message
    requests.post(config.url + 'channel/join/v2',
                        json={'token': token_2,
                        'channel_id': channel_id})

    # raise access error if user2 is trying to edit user1's message
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_2, 'message_id': message_id, 
                          'message': 'attempt'})
 
    assert resp.status_code == STATUS_ACCESS_ERR # raise access error

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_successful_message_edit_owner(
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message editing is successful """
    
    # the authorised user has owner permissions in the channel/DM

    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    channel_id = clear_register_two_createchanneldm_sendmsg[2]

    # user 2 joins channel 1 
    requests.post(config.url + 'channel/join/v2',
                        json={'token': token_2,
                        'channel_id': channel_id})

    # user 2 sends a message in the channel 
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 'channel_id': channel_id, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # successful edit when user 1 who is the owner edits user2's message
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_1, 'message_id': message_id_2, 
                          'message': 'attempt'})
 
    assert resp.status_code == STATUS_OK

    # successful edit when user 2 tries to edit user2's message
    resp1 = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_2, 'message_id': message_id_2, 
                          'message': 'attempt'})
 
    assert resp1.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_successful_message_edit_global_owner(\
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message editing is successful """
    
    # the authorised user has owner permissions in the channel/DM

    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # user2 creates private channel 2 and becomes owner of that channel
    create_channel_2 = requests.post(config.url + 'channels/create/v2',
                            json={'token': token_2, 'name': 'channel_2',
                                    'is_public': False})
    channel_2_data = create_channel_2.json()
    channel_id_2 = channel_2_data['channel_id'] 

    # user 1 joins channel 2 
    requests.post(config.url + 'channel/join/v2',
                        json={'token': token_1,
                        'channel_id': channel_id_2})

    # user 2 sends a message in channel 2
    send_message = requests.post(config.url + 'message/send/v1', 
                          json={'token': token_2, 
                          'channel_id': channel_id_2, 
                          'message': 'hewwoagain'})
    message = send_message.json()
    message_id_2 = message['message_id']

    # successful edit when user 1 who is the owner edits user2's message 
    # since user 1 is global owner, for empty string case as well
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_1, 'message_id': message_id_2,
                          'message': 'edit'})
 
    assert resp.status_code == STATUS_OK

    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_1, 'message_id': message_id_2,
                          'message': ''})
 
    assert resp.status_code == STATUS_OK
    
@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_edit_empty(clear_register_two_createchanneldm_sendmsg):
    """ testing if entered message is empty, the message is put """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_message_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_message_id = clear_register_two_createchanneldm_sendmsg[5]
  
    # test successful run when message is empty
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': chan_message_id, 
                          'message': ''})
 
    assert resp.status_code == STATUS_OK

    # message will no longer exist
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': chan_message_id, 
                          'message': 'hewwo'})
 
    assert resp.status_code == STATUS_INPUT_ERR

    # test dm case
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': dm_message_id, 
                          'message': ''})
 
    assert resp.status_code == STATUS_OK

    # message will no longer exist
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token, 'message_id': dm_message_id, 
                          'message': 'hewwo'})
 
    assert resp.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_dm_successful_message_edit_by_user(
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by user who sent the message 
    """
    
    message_id =  clear_register_two_createchanneldm_sendmsg[5]
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']

    # successful removal when user 2 tries to edit own message in dm
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_2, 'message_id': message_id, 
                          'message': 'edit'})
 
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_dm_successful_message_edit_by_owner(
    clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by owner """
    
    message_id =  clear_register_two_createchanneldm_sendmsg[5]
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']

    # successful edit when user 1 who is owner of dm tries to edit message in dm
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_1, 'message_id': message_id,
                          'message': 'edit'})
 
    assert resp.status_code == STATUS_OK

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_dm_fail_message_edit(clear_register_two_createchanneldm_sendmsg):
    """ testing if message removing is successful by user who sent the message 
    """
    token_1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token_2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    dm_id = clear_register_two_createchanneldm_sendmsg[4]
    # create user 3
    user3 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'iii@def.com', 'password': 'password',
                        'name_first': 'first3', 'name_last': 'last3'})
 
    assert user3.status_code == STATUS_OK
    user_3 = user3.json()

    # user 1 sends message in dm
    send_message = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token_1,
                                'dm_id': dm_id, 
                                'message': 'hewwooooo'})
 
    assert send_message.status_code == STATUS_OK
    dm_message = send_message.json()
    message_id = dm_message['message_id']

    # raise access error when user 2 tries to edit user 1's message
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': token_2, 'message_id': message_id,
                          'message': 'edit'})
 
    assert resp.status_code == STATUS_ACCESS_ERR

    # raise access error when user 3 tries to edit user 1's message
    resp = requests.put(config.url + 'message/edit/v1', 
                          json={'token': user_3['token'], 
                          'message_id': message_id, 'message': 'edit'})
 
    assert resp.status_code == STATUS_ACCESS_ERR

requests.delete(config.url + 'clear/v1')
