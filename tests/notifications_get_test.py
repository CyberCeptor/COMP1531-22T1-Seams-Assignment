"""
Filename: notifications_get_test.py

Author: Aleesha Bunrith(z5371516)
Created: 10/04/2022

Description: pytests for notifications/get/v1
"""

import pytest

import requests

from src import config

from src.global_vars import STATUS_OK, STATUS_INPUT_ERR, STATUS_ACCESS_ERR, \
                            EXPIRED_TOKEN, UNSAVED_TOKEN

USER1_HANDLE = 'firstlast'
USER2_HANDLE = 'firstlast0'

DM_NAME = f'{USER1_HANDLE}, {USER2_HANDLE}'
CHAN_NAME = 'channel_name'

TAGGED_NOTIF = f'{USER1_HANDLE} tagged you in {CHAN_NAME}: @{USER2_HANDLE} hewwo'
TAGGED_SELF_NOTIF = f'{USER2_HANDLE} tagged you in {DM_NAME}: @{USER2_HANDLE} hewwo'
REACT_NOTIF = f'{USER1_HANDLE} reacted to your message in {DM_NAME}'

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_notifications_get_works(clear_register_two_createchanneldm_sendmsg):
    """ test that notifications are returned correctly after a user is 
    - tagged in a message
    - their message is reacted to
    - they're added to a channel
    - they're added to a dm """

    user1 = clear_register_two_createchanneldm_sendmsg[0]
    user2 = clear_register_two_createchanneldm_sendmsg[1]
    chan_id = clear_register_two_createchanneldm_sendmsg[2]
    dm_id = clear_register_two_createchanneldm_sendmsg[4]
    dm_msg_id = clear_register_two_createchanneldm_sendmsg[5]

    # user 1 reacts with react id 1 to the dm message user 2 sent
    resp0 = requests.post(config.url + 'message/react/v1', 
                          json={'token': user1['token'], 'message_id': dm_msg_id, 
                                'react_id': 1})
    assert resp0.status_code == STATUS_OK

    resp1 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': user2['token']})
    assert resp1.status_code == STATUS_OK
    notifs = resp1.json()['notifications']

    assert len(notifs) == 5

    # notification messages in order from least recent to most recent
    dm_add_notif = f'{USER1_HANDLE} added you to {DM_NAME}'
    chan_add_notif = f'{USER1_HANDLE} added you to {CHAN_NAME}'

    # notifications are returned in order from most recent to least recent
    assert notifs[0]['notification_message'] == REACT_NOTIF
    assert notifs[0]['dm_id'] == dm_id

    assert notifs[1]['notification_message'] == TAGGED_SELF_NOTIF
    assert notifs[1]['dm_id'] == dm_id

    assert notifs[2]['notification_message'] == TAGGED_NOTIF
    assert notifs[2]['channel_id'] == chan_id

    assert notifs[3]['notification_message'] == chan_add_notif
    assert notifs[3]['channel_id'] == chan_id

    assert notifs[4]['notification_message'] == dm_add_notif
    assert notifs[4]['dm_id'] == dm_id

@pytest.mark.usefixtures('clear_register_two_createchanneldm')
def test_notifications_get_tagged_message_long(clear_register_two_createchanneldm):
    """ test that the message returned in the notification message after being
    tagged is truncated properly """

    user1 = clear_register_two_createchanneldm[0]
    user2 = clear_register_two_createchanneldm[1]
    chan_id = clear_register_two_createchanneldm[2]
    dm_id = clear_register_two_createchanneldm[3]

    message = '@firstlast0 do you have icecream?'
    notif1 = f'{USER1_HANDLE} tagged you in {CHAN_NAME}: @firstlast0 do you h'
    notif2 = f'{USER1_HANDLE} tagged you in {DM_NAME}: @firstlast0 do you h'

    # user1 sends message in channel 1, tagging user2
    resp0 = requests.post(config.url + 'message/send/v1', 
                          json={'token': user1['token'], 'channel_id': chan_id, 
                                'message': message})
    assert resp0.status_code == STATUS_OK

    resp1 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': user2['token']})
    assert resp1.status_code == STATUS_OK
    notifs = resp1.json()['notifications']

    assert len(notifs) == 3

    # tagged notification will be the most recent
    assert notifs[0]['notification_message'] == notif1
    assert notifs[0]['channel_id'] == chan_id

    # user1 sends message in dm 1, tagging user2
    resp2 = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': user1['token'], 'dm_id': dm_id, 
                                'message': message})
    assert resp2.status_code == STATUS_OK

    resp3 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': user2['token']})
    assert resp3.status_code == STATUS_OK
    notifs = resp3.json()['notifications']

    # notifications will increase by 1
    assert len(notifs) == 4

    # tagged notification will be the most recent
    assert notifs[0]['notification_message'] == notif2
    assert notifs[0]['dm_id'] == dm_id

@pytest.mark.usefixtures('clear_register_two_createchannel_join_send50msgs')
def test_notifications_get_more_than_20(clear_register_two_createchannel_join_send50msgs):
    """ test that only 20 notifications are returned"""

    token2 = clear_register_two_createchannel_join_send50msgs[1]
    
    resp = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp.status_code == STATUS_OK
    notifs = resp.json()['notifications']

    assert len(notifs) == 20

@pytest.mark.usefixtures('clear_register_two_createchanneldm_sendmsg')
def test_notifications_get_invalid_token(clear_register_two_createchanneldm_sendmsg):
    """ test that errors are raised when token input is invalid"""

    # token is int
    resp0 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': 0})
    assert resp0.status_code == STATUS_INPUT_ERR

    # token is bool
    resp1 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': True})
    assert resp1.status_code == STATUS_INPUT_ERR

    # token input empty
    resp2 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': ''})
    assert resp2.status_code == STATUS_INPUT_ERR

    # not a valid jwt token str
    resp3 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': 'str'})
    assert resp3.status_code == STATUS_ACCESS_ERR

    # expired token
    resp4 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': EXPIRED_TOKEN})
    assert resp4.status_code == STATUS_ACCESS_ERR

    # unsaved token
    resp5 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': UNSAVED_TOKEN})
    assert resp5.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm')
def test_notifications_get_user_not_member(clear_register_two_createchanneldm):
    """ test that a user doesn't receive notifications from channels or dms
    they are not a member of """

    token1 = clear_register_two_createchanneldm[0]['token']
    token2 = clear_register_two_createchanneldm[1]['token']
    chan_id = clear_register_two_createchanneldm[2]
    dm_id = clear_register_two_createchanneldm[3]

    # user2 leaves the channel
    resp0 = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token2, 
                                  'channel_id': chan_id})
    assert resp0.status_code == STATUS_OK

    # user1 sends message in channel, tagging user 2
    resp1 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token1, 'channel_id': chan_id, 
                                'message': '@firstlast0 hewwo'})
    assert resp1.status_code == STATUS_OK

    resp2 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp2.status_code == STATUS_OK
    notifs = resp2.json()['notifications']

    # user2 will only have the notification where they were invited to the 
    # channel and added to the dm
    assert len(notifs) == 2
    assert TAGGED_NOTIF not in [k['notification_message'] for k in notifs]

    # user2 sends a message in the dm
    resp3 = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token2, 'dm_id': dm_id, 
                                'message': 'bye bye'})
    assert resp3.status_code == STATUS_OK
    msg_data = resp3.json()
    msg_id = msg_data['message_id']

    # user2 leaves the dm
    resp4 = requests.post(config.url + 'dm/leave/v1', 
                            json={'token': token2, 'dm_id': dm_id})
    assert resp4.status_code == STATUS_OK

    # user1 reacts to user2's message
    resp5 = requests.post(config.url + 'message/react/v1', 
                          json={'token': token1, 'message_id': msg_id, 
                                'react_id': 1})
    assert resp5.status_code == STATUS_OK

    resp6 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp6.status_code == STATUS_OK
    notifs = resp6.json()['notifications']

    # user2 will still only have the notification where they were invited to the 
    # channel and added to the dm
    assert len(notifs) == 2
    assert REACT_NOTIF not in [k['notification_message'] for k in notifs]

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_notifications_get_invalid_handle(clear_register_two_createchannel):
    """ test that tagging an invalid handle will work but no one will receive
    a notification """

    token1 = clear_register_two_createchannel[0]['token']
    token2 = clear_register_two_createchannel[1]['token']
    channel_id = clear_register_two_createchannel[2]

    # user1 will have no notifications
    resp0 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token1})
    assert resp0.status_code == STATUS_OK
    user1_notifs1 = resp0.json()['notifications']

    assert len(user1_notifs1) == 0

    # user2 will have no notifications
    resp1 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp1.status_code == STATUS_OK
    user2_notifs1 = resp1.json()['notifications']

    assert len(user2_notifs1) == 0

    # user1 sends message in channel 1, tagging a non-existant user
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token1,
                                'channel_id': channel_id, 
                                'message': '@firstlast!@ hewwo'})
    assert resp3.status_code == STATUS_OK

    # user1 will still have no notifications
    resp0 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token1})
    assert resp0.status_code == STATUS_OK
    user1_notifs2 = resp0.json()['notifications']

    assert user1_notifs1 == user1_notifs2

    # user2 will still have no notifications
    resp1 = requests.get(config.url + 'notifications/get/v1',
                         params={'token': token2})
    assert resp1.status_code == STATUS_OK
    user2_notifs2 = resp1.json()['notifications']

    assert user2_notifs1 == user2_notifs2

requests.delete(config.url + 'clear/v1')
