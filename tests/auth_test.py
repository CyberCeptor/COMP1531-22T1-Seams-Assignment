"""
Filename: auth_test.py

Author: Aleesha Bunrith(z5371516)
Created: 24/02/2022 - 27/03/2022

Description: pytests for auth/register/v2, auth/login/v2, and auth/logout/v1
"""

import pytest

import requests

from src import config

from src.global_vars import expired_token, unsaved_token

NAME_22_CHARS = 'abcdefghijklmnopqrstuv'
NAME_52_CHARS = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'

@pytest.mark.usefixtures('clear_register')
def test_register_invalid_email(clear_register):
    """ registers a user with an invalid email and raises an InputError for each
    case """

    # no email input
    resp0 = requests.post(config.url + 'auth/register/v2',
                         json={'email': '', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 400

    # missing @ and .
    resp1 = requests.post(config.url + 'auth/register/v2',
                         json={'email': 'abc', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 400

    # missing @
    resp2 = requests.post(config.url + 'auth/register/v2',
                         json={'email': 'abc.def', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp2.status_code == 400

    # missing .
    resp3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp3.status_code == 400

    # missing characters before @
    resp4 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': '@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp4.status_code == 400

    # missing characters between @ and .
    resp5 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp5.status_code == 400

    # missing characters after .
    resp6 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp6.status_code == 400

    # numbers after .
    resp7 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.123', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp7.status_code == 400

    # email is bool
    resp7 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': True, 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp7.status_code == 400

    # email is int
    resp7 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 666, 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp7.status_code == 400

    # missing . and @
    resp8 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abcdef', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp8.status_code == 400

# based on code Haydon wrote in project starter video
@pytest.mark.usefixtures('clear_register')
def test_register_duplicate_email(clear_register):
    """ registers a user with the same email as an already registered user and
    raises an InputError """

    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp.status_code == 400

@pytest.mark.usefixtures('clear_register')
def test_register_invalid_password(clear_register):
    """ registers a user with an invalid password i.e one that is too short and
    raises an InputError """

    # password too short
    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'pass',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp.status_code == 400

@pytest.mark.usefixtures('clear_register')
def test_register_invalid_name(clear_register):
    """ registers a user with an invalid name and raises an InputError for each
    case """

    # first name too short
    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': '', 'name_last': 'last'})
    assert resp0.status_code == 400

    # last name too short
    resp1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first', 'name_last': ''})
    assert resp1.status_code == 400

    # first name too long
    resp2 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': NAME_52_CHARS, 'name_last': 'last'}
                        )
    assert resp2.status_code == 400

    # last name too long
    resp3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first',
                               'name_last': NAME_52_CHARS})
    assert resp3.status_code == 400

    # name has no letters -> would create an empty handle
    resp4 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': '-', 'name_last': ' '})
    assert resp4.status_code == 400

    # first name is a bool
    resp5 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': True, 'name_last': 'last'})
    assert resp5.status_code == 400

    # first name is an int
    resp6 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 44, 'name_last': 'last'})
    assert resp6.status_code == 400

    # last name is a bool
    resp7 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first', 'name_last': True})
    assert resp7.status_code == 400

    # last name is an int
    resp7 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 44})
    assert resp7.status_code == 400

@pytest.mark.usefixtures('clear_register')
def test_register_works(clear_register):
    """ tests if auth_register_v1 works by registering a user and logging them
    in """

    user1 = clear_register

    # get the returned data from register
    register_token = user1['token']
    register_id = user1['auth_user_id']

    # log the user in
    resp1 = requests.post(config.url + 'auth/login/v2', 
                  json={'email': 'abc@def.com', 'password': 'password'})
    assert resp1.status_code == 200

    # get the returned data from login
    login_data = resp1.json()
    login_token = login_data['token']
    login_id = login_data['auth_user_id']

    # if auth_user_ids are identical and token generated from registering is
    # different from token generated from logging in, then it is a valid login
    assert register_id == login_id
    assert register_token != login_token

@pytest.mark.usefixtures('clear_register')
def test_login_invalid(clear_register):
    """ logs a user in and raises an InputError for each invalid case """

    # email does not belong to a user
    resp0 = requests.post(config.url + 'auth/login/v2', 
                          json={'email': 'ghi@jkl.com', 'password': 'password'})
    assert resp0.status_code == 400

    # incorrect password
    resp1 = requests.post(config.url + 'auth/login/v2', 
                          json={'email': 'abc@def.com', 'password': 'wordpass'})
    assert resp1.status_code == 400

@pytest.mark.usefixtures('clear_register')
def test_logout_works(clear_register):
    """ tests logout works """
    token = clear_register['token']

    resp = requests.post(config.url + 'auth/logout/v1', json={'token': token})
    assert resp.status_code == 200

@pytest.mark.usefixtures('clear_register')
def test_logout_user_logged_out(clear_register):
    """ tests that the token of a user who has been logged out cannot be used
    again """

    token = clear_register['token']

    # log user out
    resp0 = requests.post(config.url + 'auth/logout/v1', json={'token': token})
    assert resp0.status_code == 200

    # user cannot be logged out again since the token is now invalid
    resp1 = requests.post(config.url + 'auth/logout/v1', json={'token': token})
    assert resp1.status_code == 403

@pytest.mark.usefixtures('clear_register')
def test_logout_invalid_token(clear_register):
    """ tests logout with invalid token inputs """

    # input error: int is passed in as token
    resp0 = requests.post(config.url + 'auth/logout/v1', json={'token': 1})
    assert resp0.status_code == 400

    # access error: non-jwt token str is passed in as token
    resp1 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': 'not a valid jwt token str'})
    assert resp1.status_code == 403

    # input error: bool is passed in as token
    resp2 = requests.post(config.url + 'auth/logout/v1', json={'token': True})
    assert resp2.status_code == 400

    # access error: expired, unsaved token
    resp3 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': expired_token})
    assert resp3.status_code == 403

    # access error: unexpired, unsaved token
    resp4 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': unsaved_token})
    assert resp4.status_code == 403

requests.delete(config.url + 'clear/v1')
