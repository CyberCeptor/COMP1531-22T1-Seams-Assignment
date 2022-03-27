"""
Filename: user_profile_setname_test.py

Author: Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: pytests for user_profile_setname__v1
"""

import pytest
import requests
from src import config

@pytest.mark.usefixtures('clear_register_two')
def test_user_setname_working(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # create a channel, add the other user as an owner aswell, 
    # to Test that all information is updated
    channel1 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1['token'], 'name': 'channel_name', 'is_public': True})
    assert channel1.status_code == 200
    channel1 = channel1.json()
    channel_id = channel1['channel_id']

    # Add the 2nd user to the channel
    join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2['token'], 'channel_id': channel_id})
    assert join.status_code == 200

    # add them as an owner of the channel
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1['token'], 'channel_id': channel_id, 'u_id': user2['auth_user_id']})
    assert addowner.status_code == 200

    # changing the name address of both users.
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'firsta', 'name_last': 'lasta'})
    assert setname.status_code == 200

    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user2['token'], 'name_first': 'first2a', 'name_last': 'last2b'})
    assert setname.status_code == 200

    # test using the name that user1 previously had.
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user2['token'], 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 200

    # Assert that the all_members and owner_members channel name has also been updated
    # check the data in the channel is correct
    detail_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1['token'], 'channel_id': channel1['channel_id']})
    detail_json = detail_details.json()

    assert len(detail_json['owner_members']) == 2
    assert len(detail_json['all_members']) == 2

    assert 'firsta' in [k['name_first'] for k in detail_json['owner_members']]
    assert 'firsta' in [k['name_first'] for k in detail_json['all_members']]
    assert 'lasta' in [k['name_last'] for k in detail_json['owner_members']]
    assert 'lasta' in [k['name_last'] for k in detail_json['all_members']]

@pytest.mark.usefixtures('clear_register_two')
def test_user_setname_working_dm(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # create a dm, add the other user aswell, 
    # to Test that all information is updated
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': user1['token'], 'u_ids': [user2['auth_user_id']]})
    assert create.status_code == 200
    dm_1 = create.json()
    dm_id = dm_1['dm_id']

    # changing the name address of both users.
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'firsta', 'name_last': 'lasta'})
    assert setname.status_code == 200

    # Assert that the all_members and owner_members dm name has also been updated
    # check the data in the dm is correct
    detail = requests.get(config.url + 'dm/details/v1', 
                        params={'token': user1['token'], 'dm_id': dm_id})
    assert detail.status_code == 200
    detail_json = detail.json()

    assert len(detail_json['members']) == 2

    assert 'firsta' in [k['name_first'] for k in detail_json['members']]
    assert 'lasta' in [k['name_last'] for k in detail_json['members']]

@pytest.mark.usefixtures('clear_register_two')
def test_user_profile_setname_bad_name_first(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # test users name_first
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 200

    # test another name_first with 2nd user
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user2['token'], 'name_first': 'first2', 'name_last': 'last'})
    assert setname.status_code == 200

    # test empty string
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': '', 'name_last': 'last'})
    assert setname.status_code == 400

    # test boolean 
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': True, 'name_last': 'last'})
    assert setname.status_code == 400

    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': False, 'name_last': 'last'})
    assert setname.status_code == 400

    # test < 1 character
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 0, 'name_last': 'last'})
    assert setname.status_code == 400

    # test > 50 characters
    name51 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': name51, 'name_last': 'last'})
    assert setname.status_code == 400

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_two')
def test_user_profile_setname_bad_name_last(clear_register_two):
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # test users name_last
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 200

    # test another name_last with 2nd user
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user2['token'], 'name_first': 'first', 'name_last': 'last2'})
    assert setname.status_code == 200

    # test empty string
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': ''})
    assert setname.status_code == 400

    # test boolean 
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': True})
    assert setname.status_code == 400

    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': False})
    assert setname.status_code == 400

    # test < 1 character
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': 0})
    assert setname.status_code == 400

    # test > 50 characters
    name51 = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': user1['token'], 'name_first': 'first', 'name_last': name51})
    assert setname.status_code == 400

    requests.delete(config.url + 'clear/v1')

@pytest.mark.usefixtures('clear_register_two')
def test_user_setname_bad_token(clear_register_two):
    # test empty token
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': '', 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 400

    # test accesserror token string
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': 'string', 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 403

    # test positive number token
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': 444, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 400

    # test negative number token
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': -1, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 400

    # test bool token
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': True, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 400

    # test expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
        MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjo\
            xNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': expired_token, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 403

    # test unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
        eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN\
            0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    setname = requests.put(config.url + 'user/profile/setname/v1', 
                            json={'token': unsaved_token, 'name_first': 'first', 'name_last': 'last'})
    assert setname.status_code == 403

    requests.delete(config.url + 'clear/v1')
