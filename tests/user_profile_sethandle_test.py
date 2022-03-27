"""
Filename: user_profile_sethandle_test.py

Author: Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: pytests for user_profile_sethandle_v1
"""

import pytest
import requests
from src import config

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: user_data in json form.
    """
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last', 'handle_str': 'handle'})
    user1_json = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password2',
                        'name_first': 'first2', 'name_last': 'last2', 'handle_str': 'handle2'})
    user2_json = user2.json()
    
    return [user1_json, user2_json]

def test_user_sethandle_working(clear_and_register):
    user1 = clear_and_register[0]
    user2 = clear_and_register[1]

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

    # changing the handle_str of both users.
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': 'handle3'})
    assert sethandle.status_code == 200

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user2['token'], 'handle_str': 'handle4'})
    assert sethandle.status_code == 200

    # test using the handle_str that user1 previously had.
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user2['token'], 'handle_str': 'handle'})
    assert sethandle.status_code == 200

    # Assert that the all_members and owner_members channel handle_str has also been updated
    # check the data in the channel is correct
    channels_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1['token'], 'channel_id': channel1['channel_id']})
    channels_json = channels_details.json()

    assert len(channels_json['owner_members']) == 2
    assert len(channels_json['all_members']) == 2

    assert channels_json['owner_members'][0]['handle_str'] == 'handle3'
    assert channels_json['all_members'][0]['handle_str'] == 'handle3'

    assert channels_json['owner_members'][1]['handle_str'] == 'handle'
    assert channels_json['all_members'][1]['handle_str'] == 'handle'

def test_user_profile_sethandle_bad_handle_str(clear_and_register):
    user1 = clear_and_register[0]
    user2 = clear_and_register[1]

    # test another handle_str
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': 'handle'})
    assert sethandle.status_code == 200

    # test another handle_str with 2nd user
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user2['token'], 'handle_str': 'handle'})
    assert sethandle.status_code == 400

    # test not alphanumeric handle_str
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': '$%*$^&$'})
    assert sethandle.status_code == 400

    # test empty string
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': ''})
    assert sethandle.status_code == 400

    # test boolean 
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': True})
    assert sethandle.status_code == 400

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': False})
    assert sethandle.status_code == 400

    # test < 3 int
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': 2})
    assert sethandle.status_code == 400

    # test > 20 int
    string21 = 'abcdefghijklmnopqrstuvwxyz'
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': user1['token'], 'handle_str': string21})
    assert sethandle.status_code == 400

    requests.delete(config.url + 'clear/v1')

def test_user_sethandle_bad_token(clear_and_register):
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': '', 'handle_str': 'handle'})
    assert sethandle.status_code == 400

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': 'string', 'handle_str': 'handle'})
    assert sethandle.status_code == 403

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': 444, 'handle_str': 'handle'})
    assert sethandle.status_code == 400

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': -1, 'handle_str': 'handle'})
    assert sethandle.status_code == 400

    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': True, 'handle_str': 'handle'})
    assert sethandle.status_code == 400

    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
        MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjo\
            xNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': expired_token, 'handle_str': 'handle'})
    assert sethandle.status_code == 403

    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
        eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN\
            0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    sethandle = requests.put(config.url + 'user/profile/sethandle/v1', 
                            json={'token': unsaved_token, 'handle_str': 'handle'})
    assert sethandle.status_code == 403

    requests.delete(config.url + 'clear/v1')