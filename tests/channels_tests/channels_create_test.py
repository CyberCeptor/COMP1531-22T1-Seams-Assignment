"""
Filename: channels_create_test.py

Author: Jenson Morgan(z5360181), Aleesha Bunrith(z5371516)
Created: 28/02/2022 - 27/03/2022

Description: pytests for channels_create_v1
"""

import pytest

import requests

from src import config

from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register')
def test_channels_create_invalid_token(clear_register):
    """ Registers a valid user, and them attempts to create multiple channels
    with invalid token values, both public and private channels. """
    
    # token is an integer value
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 2, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp0.status_code == STATUS_INPUT_ERR

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 2, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp1.status_code == STATUS_INPUT_ERR

    # token is a boolean value
    resp2 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': True, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp2.status_code == STATUS_INPUT_ERR

    resp3 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': True, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp3.status_code == STATUS_INPUT_ERR

    # token is a string but not a jwt token string
    resp4 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 'normal_string',
                                'name': 'test_channel_public',
                                'is_public': True})
    assert resp4.status_code == STATUS_ACCESS_ERR

    resp5 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': 'normal_string',
                                'name': 'test_channel_private',
                                'is_public': False})
    assert resp5.status_code == STATUS_ACCESS_ERR
        
    # access error: an expired token
    resp6 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': EXPIRED_TOKEN,
                                 'name': 'test_channel_public',
                                 'is_public': True})
    assert resp6.status_code == STATUS_ACCESS_ERR

    resp7 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': EXPIRED_TOKEN,
                                 'name': 'test_channel_private',
                                 'is_public': False})
    assert resp7.status_code == STATUS_ACCESS_ERR

    # access error: an unsaved token
    resp8 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': UNSAVED_TOKEN,
                                 'name': 'test_channel_public',
                                 'is_public': True})
    assert resp8.status_code == STATUS_ACCESS_ERR

    resp8 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': UNSAVED_TOKEN,
                                 'name': 'test_channel_private',
                                 'is_public': False})
    assert resp8.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register')
def test_channels_create_too_short(clear_register):
    """ Create a channel with no channel name given. Tests both public and
    private channels. """
     
    token = clear_register['token']
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': '', 'is_public': True})
    assert resp0.status_code == STATUS_INPUT_ERR

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': '', 'is_public': False})
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register')
def test_channels_create_invalid_name(clear_register):
    """ Creates a public/private channel with names > 20 characters """
     
    token = clear_register['token']
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'MoreThan20CharPublic!',
                                'is_public': True})
    assert resp0.status_code == STATUS_INPUT_ERR

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'MoreThan20CharPrivate',
                                'is_public': False})
    assert resp1.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register')
def test_channels_create_boolean(clear_register):
    """ Creates a channel with a string as the is_public argument, which should
    be a boolean. """
     
    token = clear_register['token']

    # string
    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel',
                                'is_public': 'Not a boolean'})
    assert resp0.status_code == STATUS_INPUT_ERR

    # int
    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel',
                                'is_public': 1})
    assert resp1.status_code == STATUS_INPUT_ERR

    # empty string
    resp2 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel',
                                'is_public': ''})
    assert resp2.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register')
def test_channels_duplicate_name(clear_register):
    """ Creates a channel with an existing channel_name. Both public and private
    """
     
    token = clear_register['token']

    resp0 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp0.status_code == STATUS_OK

    resp1 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_public',
                                'is_public': True})
    assert resp1.status_code == STATUS_INPUT_ERR

    resp2 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp2.status_code == STATUS_OK

    resp3 = requests.post(config.url + 'channels/create/v2', 
                          json={'token': token, 'name': 'test_channel_private',
                                'is_public': False})
    assert resp3.status_code == STATUS_INPUT_ERR

requests.delete(config.url + 'clear/v1')
