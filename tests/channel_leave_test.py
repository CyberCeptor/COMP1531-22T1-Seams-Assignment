import pytest
import requests

from src import config


@pytest.fixture(name='clear_and_register_create')
def fixture_clear_and_register_create():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    user_json = user.json()

    channel = requests.post(config.url + 'channels/create/v2', 
                          json={'token': user_json['token'], 'name': 'test_channel_public',
                                'is_public': True})
    assert channel.status_code == 200
    channel_json = channel.json()

    return [user_json['token'], channel_json['channel_id']]


# Working test case
def test_channel_leave_works(clear_and_register_create):
    token = clear_and_register_create[0]
    channel_id = clear_and_register_create[1]
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token, 'channel_id': channel_id})
    assert channel_leave.status_code == 200


def test_channel_leave_unknown_user(clear_and_register_create):
    channel_id = clear_and_register_create[1]

    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password',
                        'name_first': 'first2', 'name_last': 'last2'})
    user2_json = user2.json()

    # User NOT in the channel
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': channel_id})
    assert channel_leave.status_code == 403



def test_channel_leave_invalid_channel_id(clear_and_register_create):
    # creating 2 users and the channel.
    token = clear_and_register_create[0]
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
def test_channel_leave_invalid_token(clear_and_register_create):
    channel_id = clear_and_register_create[1]
    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
        MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjo\
            xNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': expired_token, 'channel_id': channel_id})
    assert channel_leave.status_code == 403

    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
        eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN\
            0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
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
