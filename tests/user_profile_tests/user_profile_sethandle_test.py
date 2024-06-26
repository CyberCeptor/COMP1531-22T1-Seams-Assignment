"""
Filename: user_profile_sethandle_test.py

Author: Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: pytests for user_profile_sethandle_v1
"""

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_user_sethandle_working(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # create a channel, add the other user as an owner aswell, 
    # to Test that all information is updated
    channel1 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1['token'], 
                                'name': 'channel_name', 'is_public': True})
    assert channel1.status_code == STATUS_OK
    channel1 = channel1.json()
    channel_id = channel1['channel_id']

    # Add the 2nd user to the channel
    join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2['token'], 
                                'channel_id': channel_id})
    assert join.status_code == STATUS_OK

    # add them as an owner of the channel
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1['token'], 'channel_id': channel_id, 
                                'u_id': user2['auth_user_id']})
    assert addowner.status_code == STATUS_OK

    # changing the handle_str 
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_OK

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user2['token'], 
                                    'handle_str': 'handle2'})
    assert sethandle.status_code == STATUS_OK

    # Assert that the all_members and owner_members channel handle_str has also been updated
    # check the data in the channel is correct
    channels_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1['token'], 
                                    'channel_id': channel1['channel_id']})
    channels_json = channels_details.json()

    assert len(channels_json['owner_members']) == 2
    assert len(channels_json['all_members']) == 2

    assert 'handle' in [k['handle_str'] for k in channels_json['owner_members']]
    assert 'handle' in [k['handle_str'] for k in channels_json['all_members']]
    assert 'handle2' in [k['handle_str'] for k in channels_json['owner_members']]
    assert 'handle2' in [k['handle_str'] for k in channels_json['all_members']]

@pytest.mark.usefixtures('clear_register_two')
def test_user_profile_sethandle_bad_handle_str(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # test handle_str
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_OK

    # test the handle is already used by another user
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user2['token'], 
                                    'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test not alphanumeric handle_str
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': '!@#$%^&*()_+'})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test empty string
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': ''})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test boolean 
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': True})
    assert sethandle.status_code == STATUS_INPUT_ERR

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': False})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test < 3 characters
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': 2})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test > 20 characters
    string21 = 'abcdefghijklmnopqrstuvwxyz'
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': string21})
    assert sethandle.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_user_sethandle_bad_token(clear_register_two):
    # test empty token
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': '', 'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test accesserror token string
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': 'string', 'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_ACCESS_ERR

    # test positive number token
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': 444, 'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test negative number token
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': -1, 'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test bool token
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': True, 'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_INPUT_ERR

    # test expired token
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': EXPIRED_TOKEN, 
                                    'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_ACCESS_ERR

    # test unsaved token
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': UNSAVED_TOKEN, 
                                    'handle_str': 'handle'})
    assert sethandle.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_user_profile_sethandle_duplicate_handle_str(clear_register_two):
    user1 = clear_register_two[0]

    # test another handle_str in channel
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 
                                    'handle_str': 'firstlast0'})
    assert sethandle.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_user_sethandle_working_dm(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # create a dm, add the other user aswell,
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': user1['token'], 
                                'u_ids': [user2['auth_user_id']]})
    assert create.status_code == STATUS_OK

    # test change another handle_str in dm
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user2['token'],
                                    'handle_str': 'first2last22222'})
    assert sethandle.status_code == STATUS_OK

requests.delete(config.url + 'clear/v1')
