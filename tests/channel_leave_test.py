import pytest
import requests
import json
from src import config
from src.error import AccessError, InputError
from src.channels import channels_create_v1


@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
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
    return user_json



def test_channel_leave(clear_and_register):
    """
    Create 2 users, first users creates a channel.
    the 2nd user tries to leave the channel, with an error.


    """
    user1_json = clear_and_register
    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password',
                        'name_first': 'first2', 'name_last': 'last2'})
    user2_json = user2.json()

    channel = requests.post(config.url + 'channels/create/v2', 
                          json={'token': user1_json['token'], 'name': 'test_channel_public',
                                'is_public': True})
    assert channel.status_code == 200
    channel_json = channel.json()



    ##################### Bad Channel id tests.

    # User NOT in the channel
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 403

    # Incorrect channel id
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': channel_json['channel_id'] + 4})
    assert channel_leave.status_code == 400

    # Incorrect channel id, empty string
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': ''})
    assert channel_leave.status_code == 403

    # Incorrect channel id as bool
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': True})
    assert channel_leave.status_code == 403

    # Incorrect channel id as negative number
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user2_json['token'], 'channel_id': -1})
    assert channel_leave.status_code == 403

    
    ################### Bad Token Tests

    # expired token
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
        MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjo\
            xNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': expired_token, 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 403

    # unsaved token
    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
        eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN\
            0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': unsaved_token, 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 403

    # Input Error token int
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': 4444, 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 400

    # Input error token bool
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': True, 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 400

    # Input error token empty string
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': '', 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 400

    # Input error token empty string
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': 'bad_token', 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 403






    # Working test case
    channel_leave = requests.post(config.url + 'channel/leave/v1', 
                            json={'token': user1_json['token'], 'channel_id': channel_json['channel_id']})
    assert channel_leave.status_code == 200

    # Could check channel_details to ensure the user has been removed, 
    # or that the channel has been removed if thats whats required when there are no users.