import pytest
import requests

from src import config


@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_leave_works(clear_register_createchannel):
    token = clear_register_createchannel[0]['token']
    channel_id = clear_register_createchannel[1]

    create_user2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'xue2@gmail.com', 'password': 'xzq19112',
                                'name_first': 'Xue', 'name_last':'zhiqian'})
    user2 = create_user2.json()
    token2 = user2['token']

    join_2 = requests.post(config.url + 'channel/join/v2',
                        json={'token': token2, 'channel_id': channel_id})
    assert join_2.status_code == 200
    
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token2, 'channel_id': channel_id})
    assert channel_leave.status_code == 200

    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': token, 'channel_id': channel_id})
    assert channel_leave.status_code == 200

@pytest.mark.usefixtures('clear_register_createchannel')
def test_channel_leave_unknown_user(clear_register_createchannel):
    channel_id = clear_register_createchannel[1]

    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password',
                        'name_first': 'first2', 'name_last': 'last2'})
    user2_json = user2.json()

    # User NOT in the channel
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
