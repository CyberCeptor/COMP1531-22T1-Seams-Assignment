"""
Filename: channels_test.py

Author: Jenson Morgan(z5360181)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channels_create_v1
"""

import pytest

import requests

from src import config

from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channels import channels_create_v1

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """
    clears any data stored in data_stored and registers a user with the
    given information
    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    # clear_v1()
    # user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    # return user1
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    data = resp.json()
    token = data['token']
    return token



#   NOT USED ANYMORE.
########################################################################

# def test_channels_create_valid_auth_id(clear_and_register):
#     """
#     Registers a valid user, and them
#     attempts to create 4 channels with unregistered user_id's,
#     both public and private channels.

#     Arguments: clear_and_register

#     Exceptions:
#         AccessError - Raised for all tests below

#     Return Value: N/A
#     """
#     # pylint: disable=unused-argument
#     with pytest.raises(AccessError):
#         channels_create_v1(2, 'test_channel_public', True)
#     with pytest.raises(AccessError):
#         channels_create_v1(2, 'test_channel_private', False)
#     with pytest.raises(InputError):
#         channels_create_v1(-2, 'test_channel_public2', True)
#     with pytest.raises(InputError):
#         channels_create_v1(-2, 'test_channel_private2', False)
#     with pytest.raises(InputError):
#         channels_create_v1('', 'test_channel_private2', False)
#     with pytest.raises(InputError):
#         channels_create_v1('not int', 'test_channel_private2', False)
#     with pytest.raises(InputError):
#         channels_create_v1(True, 'test_channel_private2', False)
###################################################################################


def test_channels_create_valid_token(clear_and_register):
    """
    Registers a valid user, and them
    attempts to create multipole channels with invalid token values,
    both public and private channels.

    Arguments: clear_and_register

    Exceptions:
        AccessError - Raised for all tests below

    Return Value: N/A
    """
    # pylint: disable=unused-argument
    # token is an integer value
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 2, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp0.status_code == 400

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 2, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp1.status_code == 400

    # token is a boolean value
    resp2 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': True, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp2.status_code == 400

    resp3 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': True, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp3.status_code == 400

    # token is a string but not a jwt token string
    resp4 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 'normal_string',
                                'name': 'test_channel_public',
                                'is_public': True})
    assert resp4.status_code == 403

    resp5 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 'normal_string',
                                'name': 'test_channel_private',
                                'is_public': False})
    assert resp5.status_code == 403
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc\
        2lvbl9pZCI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3\
            OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'
            
    resp6 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': expired_token,
                                 'name': 'test_channel_private',
                                 'is_public': False})
    assert resp6.status_code == 403

def test_channels_create_too_short(clear_and_register):
    """
    Create a channel with no channel name given.
        Tests both public and private channels.

    Arguments: clear_and_register

    Exceptions:
        InputError  - Raised for all cases below

    Return Value:   N/A
    """
    # id1 = clear_and_register['auth_user_id']
    # # Testing channel name is less than 1 character. Input Error
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, '', True)
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, '', False)
    token = clear_and_register
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': '', 'is_public': True})
    assert resp0.status_code == 400

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': '', 'is_public': False})
    assert resp1.status_code == 400

def test_channels_create_invalid_name(clear_and_register):
    """
    Creates a public/private channel with names > 20 characters

    Arguments:  clear_and_register

    Exceptions:
        InputError  -   Raised for all tests below

    Return Value:   N/A
    """
    # id1 = clear_and_register['auth_user_id']
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, 'MoreThan20CharPublic!', True)
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, 'MoreThan20CharPrivate', False)
    token = clear_and_register
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'MoreThan20CharPublic!',
                                'is_public': True})
    assert resp0.status_code == 400

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'MoreThan20CharPrivate',
                                'is_public': False})
    assert resp1.status_code == 400

def test_channels_create_boolean(clear_and_register):
    """
    Creates a channel with a string as the is_public argument,
        which should be a boolean.

    Arguments:  clear_and_register

    Exceptions:
        InputError - Raised for the case

    Return Value:   N/A
    """
    # id1 = clear_and_register['auth_user_id']
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, 'test_channel', 'Not a boolean')
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, 'test_channel', 1)
    token = clear_and_register
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel',
                                'is_public': 'Not a boolean'})
    assert resp0.status_code == 400

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel',
                                'is_public': 1})
    assert resp1.status_code == 400

def test_channels_duplicate_name(clear_and_register):
    """
    Creates a channel with an existing channel_name
        Both public and private

    Arguments:  clear_and_register

    Exceptions:
        InputError  -   Raised for all test cases below
    """
    # id1 = clear_and_register['auth_user_id']
    # channels_create_v1(id1, 'test_channel_public', True)
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, 'test_channel_public', True)

    # channels_create_v1(id1, 'test_channel_private', False)
    # with pytest.raises(InputError):
    #     channels_create_v1(id1, 'test_channel_private', False)
    token = clear_and_register
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp0.status_code == 200

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp1.status_code == 400

    resp2 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp2.status_code == 200

    resp3 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_public',
                                'is_public': False})
    assert resp3.status_code == 400

# clear_v1()
requests.delete(config.url + 'clear/v1')
