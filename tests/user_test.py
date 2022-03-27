import pytest
import requests

from src import config

@pytest.mark.usefixtures('clear_register')
def test_user_profile_working(clear_register):
    """
    Create two users,
    then calls user_profile_v1 with the token of the first user,
    and the id of the second user.
    Returns the info of the ID given. (i.e., the second user)
    """

    user0_json = clear_register

    user1 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'def@abc.com', 'password': 'password',
                        'name_first': 'first0', 'name_last': 'last0'})
                    
    assert user1.status_code == 200
    user1_json = user1.json()

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user1_json['token'], 'u_id': user0_json['auth_user_id']})
    assert user_profile.status_code == 200

    assert user_profile.json() == {
        'u_id': user0_json['auth_user_id'],
        'email': 'abc@def.com',
        'name_first': 'first',
        'name_last': 'last',
        'handle_str': 'firstlast',
    }

@pytest.mark.usefixtures('clear_register')
def test_profile_bad_token_input(clear_register):
    """
    Calls user_profile with a bad token:
        -   a string
        -   an int
        -   a boolean
        -   an empty string
        -   an expired token
        -   an unsaved token
    """

    '''Testing with a bad token'''
    user_json = clear_register
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': 'bad_token', 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403

    '''tesing with a bad token as int'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': 4444, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400

    
    '''tesing with a bad token as bool'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': True, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400

    
    '''tesing with a bad token as an empty string'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': '', 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 400


    '''token expired and unsaved'''
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6\
        MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjo\
            xNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': expired_token, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403

    '''not expired, unsaved'''
    not_expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.\
        eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN\
            0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPWiR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': not_expired_token, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403


@pytest.mark.usefixtures('clear_register')
def test_profile_bad_u_id_input(clear_register):
    """
    Calls user_profile with a bad user_id:
        -   an invalid user_id, not in the data_store
        -   a negative int
        -   a boolean
        -   an empty string
        -   a string
    """

    user_json = clear_register
    '''tesing with a bad id as an int'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': 100})
    assert user_profile.status_code == 400

    '''tesing with a bad id as a negative int'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': -100})
    assert user_profile.status_code == 400
    
    '''tesing with a bad user_id as bool'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': True})
    assert user_profile.status_code == 400

    '''tesing with a bad user_id as bool'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': False})
    assert user_profile.status_code == 400

    '''tesing with a bad user_id as an empty string'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': ''})
    assert user_profile.status_code == 400

    '''tesing with a bad user_id as a string'''
    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user_json['token'], 'u_id': 'bad_user_id'})
    assert user_profile.status_code == 400