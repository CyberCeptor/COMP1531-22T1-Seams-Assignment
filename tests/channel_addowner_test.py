"""
Filename: channel_addowner_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 27/03/2022

Testing channel_addowner works.
tests its working, bad inputs, 
unauthorised, global owners, non-members,
and non-owner_members.
"""

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_working(clear_register_two_createchannel):
    """ Creates 2 users, creates a channel with user 1,
    adds user2 to the channel,
    calls addowner with user1 token and user2 id to make user2 an owner.
    assert the channel details are correct. """

    user1_token = clear_register_two_createchannel[0]['token']
    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    user2_token = clear_register_two_createchannel[1]['token']
    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK
    # add user2 to be an owner.
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id,
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_OK

    # check the data in the channel is correct
    channels_details = requests.get(config.url + 'channel/details/v2', 
                                    params={'token': user1_token,
                                            'channel_id': channel_id})
    chan_json = channels_details.json()

    # assert the data in channels_dict matches what was given.
    assert len(chan_json['owner_members']) == 2

    assert user2_id in [k['u_id'] for k in chan_json['owner_members']]
    assert 'def@ghi.com' in [k['email'] for k in chan_json['owner_members']]
    assert 'first' in [k['name_first'] for k in chan_json['owner_members']]
    assert 'last' in [k['name_last'] for k in chan_json['owner_members']]
    assert 'firstlast0' in [k['handle_str'] for k in chan_json['owner_members']]

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_permission_id(clear_register_two_createchannel):
    """ user2 joins the channel,
    set user2 as a global owner,
    user1 leaves the channel, """

    user1_token = clear_register_two_createchannel[0]['token']
    user1_id = clear_register_two_createchannel[0]['auth_user_id']

    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    user2_token = clear_register_two_createchannel[1]['token']

    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK

    # setting user2 to global owner
    global_perm = requests.post(config.url + 'admin/userpermission/change/v1', 
                                json={'token': user1_token, 'u_id': user2_id,
                                      'permission_id': 1})
    assert global_perm.status_code == STATUS_OK

    # user1 leaves the channel, removes both all_members and owner_members
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                                  json={'token': user1_token, 
                                        'channel_id': channel_id})
    assert channel_leave.status_code == STATUS_OK

    # try and add user1 back to the channel as owner directly
    # fails because they arent a member of the channel.
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': user1_id})
    assert addowner.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_bad_channel_id(clear_register_two_createchannel):
    """ Tests channel_addowner for all possible invalid channel id inputs:
        - string
        - empty string
        - int/negative int
        - boolean """

    user1_token = clear_register_two_createchannel[0]['token']

    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    user2_token = clear_register_two_createchannel[1]['token']

    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK

    # add user2 to be an owner, with a bad channel_id
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': 444, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': -4, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': True, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': '', 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': 'string', 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_bad_user_id(clear_register_two_createchannel):
    """ Tests channel_addowner for all possible invalid user id inputs:
        - string
        - empty string
        - int/negative int
        - boolean """

    user2_token = clear_register_two_createchannel[1]['token']
    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK

    # add user2 to be an owner, with a bad user_id
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': 444})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': True})
    assert addowner.status_code == STATUS_INPUT_ERR  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': False})
    assert addowner.status_code == STATUS_INPUT_ERR  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': -1})
    assert addowner.status_code == STATUS_INPUT_ERR  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': 'string'})
    assert addowner.status_code == STATUS_INPUT_ERR  

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': ''})
    assert addowner.status_code == STATUS_INPUT_ERR  

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_not_a_member(clear_register_two_createchannel):
    """ Trying to addowner a user who is not a member of that channel.  """

    user1_token = clear_register_two_createchannel[0]['token']
    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    channel_id = clear_register_two_createchannel[2]
    
    # Adding user2 to the channel, but user1 is the only member. 
    # (i.e. user2 not a member)
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_already_an_owner(clear_register_two_createchannel):
    """ adding user2 as an owner,
    then adding them again as an owner
    InputError """

    user1_token = clear_register_two_createchannel[0]['token']

    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    user2_token = clear_register_two_createchannel[1]['token']

    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK

    # add user2 to be an owner.
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_OK

    # add user2 to be an owner AGAIN. InputError
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1_token, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_not_authorised(clear_register_two_createchannel):
    """ user2 joins the channel,
    tries to set themselves as an owner, AccessError
    user3 then tries to set themselves as owner,
    but they arent a member at all. """

    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    user2_token = clear_register_two_createchannel[1]['token']
    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK

    # add user2 to be an owner, with its own token, NOT Authorised to do so. 
    # AccessError
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user2_token, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_ACCESS_ERR

    # Random user who isnt a member of the channel
    user3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc3@def.com', 'password': 'password3',
                               'name_first': 'first3', 'name_last': 'last3'})
    user_data3 = user3.json()
    user3_token = user_data3['token']

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user3_token, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two_createchannel')
def test_channel_addowner_bad_tokens(clear_register_two_createchannel):
    """ Tests channel_addowner for all possible invalid token inputs:
        - string
        - empty string
        - int/negative int
        - boolean """

    user2_id = clear_register_two_createchannel[1]['auth_user_id']
    user2_token = clear_register_two_createchannel[1]['token']
    channel_id = clear_register_two_createchannel[2]

    # add user2 to the channel
    channel_join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token,
                        'channel_id': channel_id})
    assert channel_join.status_code == STATUS_OK

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': -1, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': '', 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': 'string', 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_ACCESS_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': True, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': False, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_INPUT_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': UNSAVED_TOKEN, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_ACCESS_ERR

    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': EXPIRED_TOKEN, 'channel_id': channel_id, 
                              'u_id': user2_id})
    assert addowner.status_code == STATUS_ACCESS_ERR

requests.delete(config.url + 'clear/v1')
