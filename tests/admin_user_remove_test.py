"""
InputError when any of:
      
        u_id does not refer to a valid user
        u_id refers to a user who is the only global owner
      
      AccessError when:
      
        the authorised user is not a global owner
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register_two_users():
    """ clears any data stored in data_store and registers a user with the
    given information """

    requests.delete(config.url + 'clear/v1')

    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200
    user1 = resp0.json()

    resp1 = requests.post(config.url + 'auth/register/v2', 
                          json={'email': 'def@ghi.com', 'password': 'password',
                                'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 200
    user2 = resp1.json()

    return [user1, user2]

def test_admin_user_remove_works(clear_and_register):
    """ user2 creates a channel and a dm and sends messages in both then gets
    removed by user1
    
    user2 will be removed from all channels and dms, their messages will be
    replaced by 'Removed user' and their email and handle can be reused
    """

    token1 = clear_and_register[0]['token']
    id1 = clear_and_register[0]['auth_user_id']

    token2 = clear_and_register[1]['token']
    id2 = clear_and_register[1]['auth_user_id']

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

    # user2 sends a message in the channel
    resp2 = requests.post(config.url + 'message/send/v1', 
                          json={'token': token2, 'channel_id': chan_id,
                                'message': 'hewwo'})
    assert resp2.status_code == 200

    # user2 also creates a dm consisting of themselves and user1,
    # and sends a message in it
    resp3 = requests.post(config.url + 'dm/create/v1', 
                          json={'token': token2, 'u_ids': [id1]})
    assert resp3.status_code == 200
    dm_data = resp3.json()
    dm_id = dm_data['dm_id']

    # resp4 = requests.post(config.url + 'message/senddm/v1', 
    #                       json={'token': token2, 'dm_id': dm_id,
    #                             'message': 'hewwooooo'})
    # assert resp4.status_code == 200

    # user1 removes user2
    resp5 = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token1, 'u_id': id2})
    assert resp5.status_code == 200

    # there will only be 1 user left
    resp6 = requests.get(config.url + 'users/all/v1', params={'token': token1})
    assert resp6.status_code == 200
    users = resp6.json()
    assert len(users['users']) == 1

    # there will only be one channel member left and no channel owners
    resp7 = requests.get(config.url + 'channel/details/v2',
                         params={'token': token1, 'channel_id': chan_id})
    assert resp7.status_code == 200
    chan_data = resp7.json()
    assert len(chan_data['owner_members']) == 0
    assert len(chan_data['all_members']) == 1

    # all channel messages will be replaced with 'Removed user'
    # i.e. the msg 'hewwo' that user2 created will be replaced
    resp8 = requests.get(config.url + 'channel/messages/v2',
                         params={'token': token1, 'channel_id': chan_id,
                                 'start': 0})
    assert resp8.status_code == 200
    chan_msgs_data = resp8.json()
    assert chan_msgs_data['messages'][0]['message'] == 'Removed user'

    # there will only be one dm member left and no channel creator
    resp9 = requests.get(config.url + 'dm/details/v1',
                         params={'token': token1, 'dm_id': dm_id})
    assert resp9.status_code == 200
    dm_data = resp9.json()
    assert len(dm_data['members']) == 1

    # all dm messages will be replaced with 'Removed user'
    # i.e. the msg 'hewwooooo' that user2 created will be replaced
    resp10 = requests.get(config.url + 'dm/messages/v1',
                         params={'token': token1, 'dm_id': dm_id, 'start': 0})
    assert resp10.status_code == 200
    chan_msgs_data = resp10.json()
    assert chan_msgs_data['messages'][0]['message'] == 'Removed user'

    # user2's profile can still be retrieved but their name_first will be
    # 'Removed' and their name_last will be 'user'
    resp11 = requests.get(config.url + 'user/profile/v1', 
                           params={'token': token1, 'u_id': id2})
    assert resp11.status_code == 200
    assert resp11.json() == {
        'u_id': id2,
        'email': 'def@ghi.com',
        'name_first': 'Removed',
        'name_last': 'user',
        'handle_str': 'firstlast0',
    }

    # user2's new profile should have the same email and handle since it is now
    # reusable
    resp12 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp12.status_code == 200
    user2_new = resp12.json()
    id2_new = user2_new['auth_user_id']
    assert id2 != id2_new

    resp13 = requests.get(config.url + 'user/profile/v1', 
                           params={'token': token1, 'u_id': id2_new})
    assert resp13.status_code == 200
    assert resp13.json() == {
        'u_id': id2_new,
        'email': 'def@ghi.com',
        'name_first': 'first',
        'name_last': 'last',
        'handle_str': 'firstlast0',
    }

def test_admin_user_remove_only_one_global_owner(clear_and_register):
    """ the only global owner is trying to remove themselves """

    token = clear_and_register[0]['token']
    id = clear_and_register[0]['auth_user_id']

    resp = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': id})
    assert resp.status_code == 400

def test_admin_user_remove_not_global_owner(clear_and_register):
    """ user 2, a normal user is trying to remove themselves """

    token = clear_and_register[1]['token']
    id = clear_and_register[1]['auth_user_id']

    resp = requests.delete(config.url + 'admin/user/remove/v1', 
                          json={'token': token, 'u_id': id})
    assert resp.status_code == 403

def test_admin_user_remove_invalid_token(clear_and_register):
    """ invalid tokens passed in """

    id2 = clear_and_register[1]['auth_user_id']

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

def test_admin_user_remove_invalid_u_id(clear_and_register):
    """ invalid u_ids passed in """

    token = clear_and_register[0]['token']

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
