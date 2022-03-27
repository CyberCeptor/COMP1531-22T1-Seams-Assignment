import pytest
import requests

from src import config
from src.global_vars import expired_token, unsaved_token

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

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': expired_token, 'u_id': user_json['auth_user_id']})
    assert user_profile.status_code == 403

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': unsaved_token, 'u_id': user_json['auth_user_id']})
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