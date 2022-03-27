"""
Filename: channel_leave_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 27/03/2022

Testing channel_leave works, 
raises errors for incorrect input format for
channel id and token, and if the user is not in the channel.
"""

import pytest
import requests

from src import config
from src.global_vars import expired_token, unsaved_token


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_leave_works(clear_register_createchannel):
    """
    Creates 2 users and a channel for user1,
    user2 joins the channel, 
    ensure that channel details matches this,
    user2 then leaves the channel,
    assert that the channel details matches this again.
    """

    user1_token = clear_register_createchannel[0]['token']
    channel_id = clear_register_createchannel[1]

    # Create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password2',
                        'name_first': 'first2', 'name_last': 'last2'})
    user2_json = user2.json()
    user2_token = user2_json['token']

    # User2 joins the channel (now a all_member)
    join_2 = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2_token, 'channel_id': channel_id})
    assert join_2.status_code == 200
    
    # Get the channel information.
    channel_details = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': user1_token, 'channel_id': channel_id})
    assert channel_details.status_code == 200
    channel_json = channel_details.json()

    # Assert user2 has joined the channel.
    assert len(channel_json['all_members']) == 2
    assert len(channel_json['owner_members']) == 1

    # User2 then leaves the channel.
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_token, 'channel_id': channel_id})
    assert channel_leave.status_code == 200

    # Get the channel information again.
    channel_details = requests.get(config.url + 'channel/details/v2', 
                          params = {'token': user1_token, 'channel_id': channel_id})
    assert channel_details.status_code == 200
    channel_json = channel_details.json()

    # Assert user2 has left the channel.
    assert len(channel_json['all_members']) == 1
    assert len(channel_json['owner_members']) == 1


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_leave_unknown_user(clear_register_createchannel):
    """
    Creates 2 users and a channel for user1,
    user2 tries to leave the channel, but they are not a member,
    AccessError.
    """
    channel_id = clear_register_createchannel[1]

    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password',
                        'name_first': 'first2', 'name_last': 'last2'})
    user2_json = user2.json()

    # User2 NOT in the channel
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': channel_id})
    assert channel_leave.status_code == 403


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_leave_invalid_channel_id(clear_register_createchannel):
    # creating 2 users and the channel.
    token = clear_register_createchannel[0]['token']

    # Incorrect channel id
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token, 'channel_id': 444})
    assert channel_leave.status_code == 400

    # Incorrect channel id, empty string
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token, 'channel_id': ''})
    assert channel_leave.status_code == 400

    # Incorrect channel id as bool
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token, 'channel_id': True})
    assert channel_leave.status_code == 400

    # Incorrect channel id as negative number
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token, 'channel_id': -1})
    assert channel_leave.status_code == 400

    
    # bad token tests.
@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_leave_invalid_token(clear_register_createchannel):
    channel_id = clear_register_createchannel[1]
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': expired_token, 'channel_id': channel_id})
    assert channel_leave.status_code == 403

    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': unsaved_token, 'channel_id': channel_id})
    assert channel_leave.status_code == 403

    # Input Error token int
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': 4444, 'channel_id': channel_id})
    assert channel_leave.status_code == 400

    # Input error token bool
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': True, 'channel_id': channel_id})
    assert channel_leave.status_code == 400

    # Input error token empty string
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': '', 'channel_id': channel_id})
    assert channel_leave.status_code == 400

    # Input error token empty string
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': 'bad_token', 'channel_id': channel_id})
    assert channel_leave.status_code == 403

requests.delete(config.url + 'clear/v1')
