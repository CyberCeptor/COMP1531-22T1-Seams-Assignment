# """
# Filename: message_share_test.py

# Author: Xingjian Dong, z5221888, Aleesha Bunrith(z5371516)
# Created: 04/04/22 - 14/04/22

# Description: pytests for
#     - share messages
# """

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of token """

    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    
    # token is int
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': 0, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is bool
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': True, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': '', 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World',
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong token input
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': 'not right string', 
                                  'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': EXPIRED_TOKEN, 
                                  'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': UNSAVED_TOKEN, 
                                  'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp5.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_invalid_og_message_id(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of og message id"""

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]

    # no og id input
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': '', 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp0.status_code == STATUS_INPUT_ERR

    # og id is bool
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': True, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp1.status_code == STATUS_INPUT_ERR

    # og id is string
    resp2 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': 'str', 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong og input
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': -5, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp3.status_code == STATUS_INPUT_ERR

    # wrong og input
    resp4 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': 100, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp4.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_invalid_message(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of message"""

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]

    # message is int
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 0, 'channel_id': chan_id, 
                                  'dm_id': -1})
    assert resp0.status_code == STATUS_INPUT_ERR

    # message is bool
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': True, 'channel_id': chan_id, 
                                  'dm_id': -1})
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_invalid_channel_id(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of channel id """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]

    # no channel id input
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': '', 
                                  'dm_id': -1})
    assert resp0.status_code == STATUS_INPUT_ERR

    # channel id is bool
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': True, 
                                  'dm_id': -1})
    assert resp1.status_code == STATUS_INPUT_ERR

    # channel id is string
    resp2 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': 'str', 
                                  'dm_id': -1})
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong channel input
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': 2, 
                                  'dm_id': -1})
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_invalid_dm_id(clear_register_two_createchanneldm_sendmsg):
    """ test for invalid input of dm id"""

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[1]

    # no dm id input
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': -1, 
                                  'dm_id': ''})
    assert resp0.status_code == STATUS_INPUT_ERR

    # dm id is bool
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': -1, 
                                  'dm_id': True})
    assert resp1.status_code == STATUS_INPUT_ERR

    # dm id is string
    resp2 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': -1, 
                                  'dm_id': 'str'})
    assert resp2.status_code == STATUS_INPUT_ERR

    # wrong dm input
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 'channel_id': -1, 
                                  'dm_id': 100})
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_both_ids_are_invalid(clear_register_two_createchanneldm_sendmsg):
    """ test for both channel_id and dm_id are invalid"""

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    dm_id = clear_register_two_createchanneldm_sendmsg[4]

    # both no channel_id and dm_id input
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_id, 
                                  'message': 'Hello World', 'channel_id': '', 
                                  'dm_id': ''})
    assert resp0.status_code == STATUS_INPUT_ERR

    # both channel_id and dm_id are bool
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_id, 
                                  'message': 'Hello World', 'channel_id': True, 
                                  'dm_id': True})
    assert resp1.status_code == STATUS_INPUT_ERR

    # both channel_id and dm_id are string
    resp2 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_id, 
                                  'message': 'Hello World', 'channel_id': 'str', 
                                  'dm_id': 'str'})
    assert resp2.status_code == STATUS_INPUT_ERR

    # neither channel_id nor dm_id are -1
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_id, 
                                  'message': 'Hello World', 'channel_id': -1, 
                                  'dm_id': -1})
    assert resp3.status_code == STATUS_INPUT_ERR

    # both channel_id and dm_id are -1
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token, 'og_message_id': chan_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': dm_id})
    assert resp3.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_invalid_length(clear_register_two_createchanneldm_sendmsg):
    """ test if input message length is valid(over 1000 char) """

    token = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]

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
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json={'token': token, 'og_message_id': chan_msg_id, 
                                'message': long_message, 'channel_id': chan_id, 
                                'dm_id': -1})
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_user_not_belong(clear_register_two_createchanneldm_sendmsg):
    """ testing if user belongs to the channel """
    
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]

    # create user 3
    user3 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 
                            'password': 'password',
                            'name_first': 'first2', 'name_last': 'last2'}) 
    assert user3.status_code == STATUS_OK
    user3_data = user3.json()
    token_3 = user3_data['token']

    # access error when user 3 tries to share message in channel 1
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token_3, 
                                  'og_message_id': chan_msg_id, 
                                  'message': 'Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp0.status_code == STATUS_ACCESS_ERR #raise access error

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_optional_msg(clear_register_two_createchanneldm_sendmsg):
    """ test for success share"""

    token1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    token2 = clear_register_two_createchanneldm_sendmsg[1]['token']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_id = clear_register_two_createchanneldm_sendmsg[4]
    dm_msg_id = clear_register_two_createchanneldm_sendmsg[5]

    resp0 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp0.status_code == STATUS_OK
    user2_notifs = resp0.json()['notifications']

    assert len(user2_notifs) == 4

    # dm is -1, user1 is tagged in optional message
    resp1 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token2, 'og_message_id': chan_msg_id, 
                                  'message': '@firstlast Hello World', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp1.status_code == STATUS_OK

    resp2 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token1})
    assert resp2.status_code == STATUS_OK
    user1_notifs = resp2.json()['notifications']

    assert len(user1_notifs) == 1

    # tag notification should be the latest
    # can't check notif message since the shared message will be different
    # depending on the notification
    assert user1_notifs[0]['channel_id'] == chan_id

    # channel is -1, user1 is tagged in optional message
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token2, 'og_message_id': dm_msg_id, 
                                  'message': '@firstlast Hello World1', 
                                  'channel_id': -1, 'dm_id': dm_id})
    assert resp3.status_code == STATUS_OK

    resp4 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token1})
    assert resp4.status_code == STATUS_OK
    user1_notifs = resp4.json()['notifications']

    assert len(user1_notifs) == 2

    # tag notification should be the latest
    # can't check notif message since the shared message will be different
    # depending on the notification
    assert user1_notifs[0]['dm_id'] == dm_id

    # user2 should receive both tag notifications for the original messages again
    resp5 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp5.status_code == STATUS_OK
    user2_notifs = resp5.json()['notifications']

    assert len(user2_notifs) == 6

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_message_share_no_optional_msg(clear_register_two_createchanneldm_sendmsg):
    """ test for success share"""

    token1 = clear_register_two_createchanneldm_sendmsg[0]['token']
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    chan_msg_id = clear_register_two_createchanneldm_sendmsg[3]
    dm_id = clear_register_two_createchanneldm_sendmsg[4]

    # dm is -1, user2 is tagged in optional message
    resp0 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token1, 'og_message_id': chan_msg_id, 
                                  'message': '', 
                                  'channel_id': chan_id, 'dm_id': -1})
    assert resp0.status_code == STATUS_OK

    # channel is -1
    resp3 = requests.post(config.url + 'message/share/v1', 
                          json = {'token': token1, 'og_message_id': chan_msg_id, 
                                  'message': '', 
                                  'channel_id': -1, 'dm_id': dm_id})
    assert resp3.status_code == STATUS_OK

requests.delete(config.url + 'clear/v1')
