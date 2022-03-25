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
                        'name_first': 'first', 'name_last': 'last'})
    user1_json = user1.json()

    user2 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc2@def.com', 'password': 'password2',
                        'name_first': 'first2', 'name_last': 'last2'})
    user2_json = user2.json()

    return [user1_json, user2_json]


def test_user_setemail_working(clear_and_register):
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


    # changing the email address of both users.
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 'abc3@def.com'})
    assert setemail.status_code == 200

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user2['token'], 'email': 'abc4@def.com'})
    assert setemail.status_code == 200

    # test using the email that user1 previously had.
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user2['token'], 'email': 'abc@def.com'})
    assert setemail.status_code == 200

    # Assert that the all_members and owner_membets channel email has also been updated
    # check the data in the channel is correct
    channels_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1['token'], 'channel_id': channel1['channel_id']})
    channels_json = channels_details.json()

    assert len(channels_json['owner_members']) == 2
    assert len(channels_json['all_members']) == 2

    assert channels_json['owner_members'][0]['email'] == 'abc3@def.com'
    assert channels_json['all_members'][0]['email'] == 'abc3@def.com'

    assert channels_json['owner_members'][1]['email'] == 'abc@def.com'
    assert channels_json['all_members'][1]['email'] == 'abc@def.com'



def test_user_setemail_bad_email(clear_and_register):
    user1 = clear_and_register[0]
    user2 = clear_and_register[1]

    # test another users email
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    # test another users email with 2nd user
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user2['token'], 'email': 'abc@def.com'})
    assert setemail.status_code == 400

    # test bad string
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 'abcdef.com'})
    assert setemail.status_code == 400

    # test empty string
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': ''})
    assert setemail.status_code == 400

    # test boolean 
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': True})
    assert setemail.status_code == 400

    # test int
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 1})
    assert setemail.status_code == 400

    # test negative int
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': -1})
    assert setemail.status_code == 400



def test_user_setemail_bad_token(clear_and_register):
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': '', 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': 'string', 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': 444, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': -1, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': True, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
        MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjo\
            xNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': expired_token, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
        eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN\
            0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': unsaved_token, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400