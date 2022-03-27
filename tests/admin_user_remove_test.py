"""
Filename: admin_user_remove_test.py

Author: Aleesha Bunrith(z5371516)
Created: 24/03/2022 - 27/03/2022

Description: pytests for admin/user/remove/v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register_two')
def test_admin_user_remove_works(clear_register_two):
    """ user2 creates a channel and a dm and sends messages in both then gets
    removed by user1
    
    user2 will be removed from all channels and dms, their messages will be
    replaced by 'Removed user' and their email and handle can be reused
    """

    token1 = clear_register_two[0]['token']
    id1 = clear_register_two[0]['auth_user_id']

    token2 = clear_register_two[1]['token']
    id2 = clear_register_two[1]['auth_user_id']

    # user2 creates a channel
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token2, 'name': 'channel',
                                'is_public': True})
    assert resp0.status_code == 200
    chan_data = resp0.json()
    chan_id = chan_data['channel_id']

    # user1 joins the channel
    resp1 = requests.post(config.url + 'channel/join/v2',
                          json={'token': token1, 'channel_id': chan_id})
    assert resp1.status_code == 200

    # there will be one owner member and two members in total
    resp2 = requests.get(config.url + 'channel/details/v2',
                         params={'token': token1, 'channel_id': chan_id})
    assert resp2.status_code == 200
    chan_data = resp2.json()
    assert len(chan_data['owner_members']) == 1
    assert len(chan_data['all_members']) == 2
    assert id2 in [k['u_id'] for k in chan_data['all_members']]
    assert id2 in [k['u_id'] for k in chan_data['owner_members']]

    # user2 sends a message in the channel
    resp3 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token2, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp3.status_code == 200

    # user2 also creates a dm consisting of themselves and user1,
    # and sends a message in it
    resp4 = requests.post(config.url + 'dm/create/v1', 
                          json={'token': token2, 'u_ids': [id1]})
    assert resp4.status_code == 200
    dm_data = resp4.json()
    dm_id = dm_data['dm_id']

    resp5 = requests.post(config.url + 'message/senddm/v1', 
                          json={'token': token2, 'dm_id': dm_id,
                                'message': 'hewwooooo'})
    assert resp5.status_code == 200

    # there will only be two dm members in total
    resp6 = requests.get(config.url + 'dm/details/v1',
                         params={'token': token1, 'dm_id': dm_id})
    assert resp6.status_code == 200
    dm_data = resp6.json()
    assert len(dm_data['members']) == 2
    assert id2 in [k['u_id'] for k in dm_data['members']]

    # user1 removes user2
    resp7 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token1, 'u_id': id2})
    assert resp7.status_code == 200

    # there will only be 1 user left
    resp8 = requests.get(config.url + 'users/all/v1', params={'token': token1})
    assert resp8.status_code == 200
    users = resp8.json()
    assert len(users['users']) == 1

    # there will only be one channel member left and no channel owners
    resp9 = requests.get(config.url + 'channel/details/v2',
                         params={'token': token1, 'channel_id': chan_id})
    assert resp9.status_code == 200
    chan_data = resp9.json()
    assert len(chan_data['owner_members']) == 0
    assert len(chan_data['all_members']) == 1
    assert id2 not in [k['u_id'] for k in chan_data['owner_members']]
    assert id2 not in [k['u_id'] for k in chan_data['all_members']]

    # all channel messages will be replaced with 'Removed user'
    # i.e. the msg 'hewwo' that user2 created will be replaced
    resp10 = requests.get(config.url + 'channel/messages/v2',
                         params={'token': token1, 'channel_id': chan_id,
                                 'start': 0})
    assert resp10.status_code == 200
    chan_msgs_data = resp10.json()
    assert id2 in [k['u_id'] for k in chan_msgs_data['messages']]
    assert 'Removed user' in [k['message'] for k in chan_msgs_data['messages']]

    # there will only be one dm member left and no channel creator
    resp11 = requests.get(config.url + 'dm/details/v1',
                         params={'token': token1, 'dm_id': dm_id})
    assert resp11.status_code == 200
    dm_data = resp11.json()
    assert len(dm_data['members']) == 1
    assert id2 not in [k['u_id'] for k in dm_data['members']]

    # all dm messages will be replaced with 'Removed user'
    # i.e. the msg 'hewwooooo' that user2 created will be replaced
    resp12 = requests.get(config.url + 'dm/messages/v1',
                         params={'token': token1, 'dm_id': dm_id, 'start': 0})
    assert resp12.status_code == 200
    dm_msgs_data = resp12.json()
    assert id2 in [k['u_id'] for k in dm_msgs_data['messages']]
    assert 'Removed user' in [k['message'] for k in dm_msgs_data['messages']]
    
    # user2's profile can still be retrieved but their name_first will be
    # 'Removed' and their name_last will be 'user'
    resp13 = requests.get(config.url + 'user/profile/v1', 
                           params={'token': token1, 'u_id': id2})
    assert resp13.status_code == 200
    profile = resp13.json()
   
    assert profile['u_id'] == id2
    assert profile['email'] == 'def@ghi.com'
    assert profile['name_first'] == 'Removed'
    assert profile['name_last'] == 'user'
    assert profile['handle_str'] == 'firstlast0'

    # user2's new profile should have the same email and handle since it is now
    # reusable
    resp14 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp14.status_code == 200
    user2_new = resp14.json()
    id2_new = user2_new['auth_user_id']
    assert id2 != id2_new

    resp15 = requests.get(config.url + 'user/profile/v1', 
                           params={'token': token1, 'u_id': id2_new})
    assert resp15.status_code == 200
    new_profile = resp15.json()
    
    assert new_profile['u_id'] == id2_new
    assert new_profile['email'] == 'def@ghi.com'
    assert new_profile['name_first'] == 'first'
    assert new_profile['name_last'] == 'last'
    assert new_profile['handle_str'] == 'firstlast0'

@pytest.mark.usefixtures('clear_register_createchannel')
def test_admin_user_remove_not_in_channel_or_dm(clear_register_createchannel):
    """ user1 removes user3, check that they are not in any channels or dms """

    token1 = clear_register_createchannel[0]['token']

    chan_id = clear_register_createchannel[1]

    # register a second user
    resp0 = requests.post(config.url + 'auth/register/v2',
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    # register a third user
    resp1 = requests.post(config.url + 'auth/register/v2',
                         json={'email': 'ghi@jkl.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 200
    user3 = resp1.json()
    id3 = user3['auth_user_id']

    # there will be one owner member and two members in total
    resp2 = requests.get(config.url + 'channel/details/v2',
                         params={'token': token1, 'channel_id': chan_id})
    assert resp2.status_code == 200
    chan_data = resp2.json()
    assert len(chan_data['owner_members']) == 1
    assert len(chan_data['all_members']) == 1

    # assert that user3 is not in the channel
    assert id3 not in [k['u_id'] for k in chan_data['all_members']]
    assert id3 not in [k['u_id'] for k in chan_data['owner_members']]

    # user1 creates a dm consisting of themselves and user1
    resp3 = requests.post(config.url + 'dm/create/v1', 
                          json={'token': token1, 'u_ids': [id2]})
    assert resp3.status_code == 200
    dm_data = resp3.json()
    dm_id = dm_data['dm_id']

    # there will only be two dm members in total
    resp4 = requests.get(config.url + 'dm/details/v1',
                         params={'token': token1, 'dm_id': dm_id})
    assert resp4.status_code == 200
    dm_data = resp4.json()
    assert len(dm_data['members']) == 2

    # check that user3 has not sent any messages in a channel
    resp6 = requests.get(config.url + 'channel/messages/v2',
                         params={'token': token1, 'channel_id': chan_id,
                                 'start': 0})
    assert resp6.status_code == 200
    chan_msgs_data = resp6.json()
    assert id3 not in [k['u_id'] for k in chan_msgs_data['messages']]

    # check that user3 has not sent any messages in a dm
    resp7 = requests.get(config.url + 'dm/messages/v1',
                         params={'token': token1, 'dm_id': dm_id, 'start': 0})
    assert resp7.status_code == 200
    dm_msgs_data = resp7.json()
    assert id3 not in [k['u_id'] for k in dm_msgs_data['messages']]

    # user1 removes user3
    resp8 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token1, 'u_id': id3})
    assert resp8.status_code == 200

@pytest.mark.usefixtures('clear_register_createchannel')
def test_admin_user_remove_no_msgs_sent(clear_register_createchannel):
    """ user1 removes user3, check that they are have no sent any messages """

    token1 = clear_register_createchannel[0]['token']

    chan_id = clear_register_createchannel[1]

    # register a second user
    resp0 = requests.post(config.url + 'auth/register/v2',
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user2 = resp0.json()
    id2 = user2['auth_user_id']

    # register a third user
    resp1 = requests.post(config.url + 'auth/register/v2',
                         json={'email': 'ghi@jkl.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 200
    user3 = resp1.json()
    id3 = user3['auth_user_id']
    token3 = user3['token']

    # user3 joins the channel
    resp2 = requests.post(config.url + 'channel/join/v2',
                          json={'token': token3, 'channel_id': chan_id})
    assert resp2.status_code == 200

    # user1 also creates a dm consisting of themselves and user3
    resp3 = requests.post(config.url + 'dm/create/v1', 
                          json={'token': token1, 'u_ids': [id3]})
    assert resp3.status_code == 200
    dm_data = resp3.json()
    dm_id = dm_data['dm_id']

    # user1 removes user3
    resp4 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token1, 'u_id': id3})
    assert resp4.status_code == 200

    # there will be one owner member left
    resp5 = requests.get(config.url + 'channel/details/v2',
                         params={'token': token1, 'channel_id': chan_id})
    assert resp5.status_code == 200
    chan_data = resp5.json()
    assert len(chan_data['owner_members']) == 1
    assert len(chan_data['all_members']) == 1

    # assert that user3 is in the channel
    assert id3 not in [k['u_id'] for k in chan_data['all_members']]
    assert id3 not in [k['u_id'] for k in chan_data['owner_members']]

    # there will only be one dm member left
    resp6 = requests.get(config.url + 'dm/details/v1',
                         params={'token': token1, 'dm_id': dm_id})
    assert resp6.status_code == 200
    dm_data = resp6.json()
    assert len(dm_data['members']) == 1

    assert id3 not in [k['u_id'] for k in dm_data['members']]

    # check that user3 has not sent any messages in the channel
    resp7 = requests.get(config.url + 'channel/messages/v2',
                         params={'token': token1, 'channel_id': chan_id,
                                 'start': 0})
    assert resp7.status_code == 200
    chan_msgs_data = resp7.json()
    assert id3 not in [k['u_id'] for k in chan_msgs_data['messages']]

    # all dm messages will be replaced with 'Removed user'
    # i.e. the msg 'hewwooooo' that user2 created will be replaced
    resp8 = requests.get(config.url + 'dm/messages/v1',
                         params={'token': token1, 'dm_id': dm_id, 'start': 0})
    assert resp8.status_code == 200
    dm_msgs_data = resp8.json()
    assert id3 not in [k['u_id'] for k in dm_msgs_data['messages']]

@pytest.mark.usefixtures('clear_register_two')
def test_admin_user_remove_only_one_global_owner(clear_register_two):
    """ the only global owner is trying to remove themselves """

    token = clear_register_two[0]['token']
    id = clear_register_two[0]['auth_user_id']

    resp = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': id})
    assert resp.status_code == 400

@pytest.mark.usefixtures('clear_register_two')
def test_admin_user_remove_not_global_owner(clear_register_two):
    """ user 2, a normal user is trying to remove themselves """

    token = clear_register_two[1]['token']
    id = clear_register_two[1]['auth_user_id']

    resp = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': id})
    assert resp.status_code == 403

@pytest.mark.usefixtures('clear_register_two')
def test_admin_user_remove_invalid_token(clear_register_two):
    """ tests user/remove with invalid token inputs """

    id2 = clear_register_two[1]['auth_user_id']

    # inpuot error: empty str is passed in as token
    resp0 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': '', 'u_id': id2})
    assert resp0.status_code == 400

    # input error: bool is passed in as token
    resp1 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': True, 'u_id': id2})
    assert resp1.status_code == 400

    # input error: int is passed in as token
    resp2 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': 400, 'u_id': id2})
    assert resp2.status_code == 400

    # input error: normal string is passed in as token
    resp3 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': 'not a jwt token str', 'u_id': id2})
    assert resp3.status_code == 403

    # access error: unexpired, unsaved token
    resp4 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': unsaved_token, 'u_id': id2})
    assert resp4.status_code == 403

    # access error: expired, unsaved token
    resp5 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': expired_token, 'u_id': id2})
    assert resp5.status_code == 403

@pytest.mark.usefixtures('clear_register_two')
def test_admin_user_remove_invalid_u_id(clear_register_two):
    """ tests user/remove with invalid u_id inputs """

    token = clear_register_two[0]['token']

    # input error: empty str is passed in as u_id
    resp0 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': ''})
    assert resp0.status_code == 400

    # input error: str is passed in as u_id
    resp1 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': 'str'})
    assert resp1.status_code == 400

    # input error: non-existent user
    resp2 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': 400})
    assert resp2.status_code == 400

    # input error: bool is passed in as u_id
    resp3 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': True})
    assert resp3.status_code == 400

    # access error: negative u_id
    resp4 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': -1})
    assert resp4.status_code == 400

requests.delete(config.url + 'clear/v1')
