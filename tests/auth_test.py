"""
Filename: auth_test.py

Author: Aleesha, z5371516
Created: 24/02/2022 - 04/03/2022

Description: pytests for auth_register_v1 and auth_login_v1
"""
import json

import pytest

import requests

from src import config

NAME_22_CHARS = 'abcdefghijklmnopqrstuv'
NAME_52_CHARS = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    # clear_v1()
    # auth_register_v1('abc@def.com', 'password', 'first', 'last')
    requests.delete(config.url + 'clear/v1')

    requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})

def test_register_invalid_email(clear_and_register):
    """ registers a user with an invalid email and raises an InputError for each
    case

    Arguments: N/A

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A """
    # pylint: disable=unused-argument

    # no email input
    # with pytest.raises(InputError):
    #     auth_register_v1('', 'password', 'first', 'last')
    resp0 = requests.post(config.url + 'auth/register/v2',
                         json={'email': '', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 400

    # missing @ and .
    # with pytest.raises(InputError):
    #     auth_register_v1('abc', 'password', 'first', 'last')
    resp1 = requests.post(config.url + 'auth/register/v2',
                         json={'email': 'abc', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp1.status_code == 400

    # missing @
    # with pytest.raises(InputError):
    #     auth_register_v1('abc.def', 'password', 'first', 'last')
    resp2 = requests.post(config.url + 'auth/register/v2',
                         json={'email': 'abc.def', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp2.status_code == 400

    # missing .
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def', 'password', 'first', 'last')
    resp3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp3.status_code == 400

    # missing characters before @
    # with pytest.raises(InputError):
    #     auth_register_v1('@def.com', 'password', 'first', 'last')
    resp4 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': '@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp4.status_code == 400

    # missing characters between @ and .
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@.com', 'password', 'first', 'last')
    resp5 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp5.status_code == 400

    # missing characters after .
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.', 'password', 'first', 'last')
    resp6 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp6.status_code == 400

    # numbers after .
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.123', 'password', 'first', 'last')
    resp7 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.123', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp7.status_code == 400

# based on code Haydon wrote in project starter video
def test_register_duplicate_email(clear_and_register):
    """ registers a user with the same email as an already registered user and
    raises an InputError

    Arguments:
        clear_and_register (fixture)

    Exceptions:
        InputError - Raised for the test case below

    Return Value: N/A """
    # pylint: disable=unused-argument

    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'password', 'first', 'last')
    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp.status_code == 400

def test_register_invalid_password(clear_and_register):
    """ registers a user with an invalid password i.e one that is too short and
    raises an InputError

    Arguments: N/A

    Exceptions:
        InputError - Raised for the test case below

    Return Value: N/A """
    # pylint: disable=unused-argument

    # password too short
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'pass', 'first', 'last')
    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'pass',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp.status_code == 400

def test_register_invalid_name(clear_and_register):
    """ registers a user with an invalid name and raises an InputError for each
    case

    Arguments: N/A

    Exceptions:
        InputError - Raised for each test case below

    Return Value: N/A """
    # pylint: disable=unused-argument

    # first name too short
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'password', '', 'last')
    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': '', 'name_last': 'last'})
    assert resp0.status_code == 400

    # last name too short
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'password', 'first', '')
    resp1 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first', 'name_last': ''})
    assert resp1.status_code == 400

    # first name too long
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'password', NAME_52_CHARS, 'last')
    resp2 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': NAME_52_CHARS, 'name_last': 'last'}
                        )
    assert resp2.status_code == 400

    # last name too long
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'password', 'first', NAME_52_CHARS)
    resp3 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': 'first',
                               'name_last': NAME_52_CHARS})
    assert resp3.status_code == 400

    # name has no letters -> would create an empty handle
    # with pytest.raises(InputError):
    #     auth_register_v1('abc@def.com', 'password', '-', ' ')
    resp4 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'def@ghi.com', 'password': 'password',
                               'name_first': '-', 'name_last': ' '})
    assert resp4.status_code == 400

# based on code Hayden wrote in project starter video
def test_register_works():
    """ tests if auth_register_v1 works by registering a user and logging them
    in

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    # clear_v1()
    # register_return = auth_register_v1('abc@def.com', 'password',
    #                                    'first', 'last')
    # auth_user_id1 = register_return['auth_user_id']
    requests.delete(config.url + 'clear/v1')
    resp0 = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    assert resp0.status_code == 200

    register_data = resp0.json()
    register_token = register_data['token']
    register_id = register_data['auth_user_id']

    # login_return = auth_login_v1('abc@def.com', 'password')
    # auth_user_id2 = login_return['auth_user_id']
    resp1 = requests.post(config.url + 'auth/login/v2', 
                  json={'email': 'abc@def.com', 'password': 'password'})
    assert resp1.status_code == 200

    login_data = resp1.json()
    login_token = login_data['token']
    login_id = login_data['auth_user_id']

    # if auth_user_ids are identical and token generated from registering is
    # different from token generated
    # from logging in, then it is a valid login
    # assert auth_user_id1 == auth_user_id2
    assert register_id == login_id
    assert register_token != login_token

def test_login_invalid(clear_and_register):
    """ logs a user in and raises an InputError for each invalid case

    Arguments:
        clear_and_register (fixture)

    Exceptions:
        InputError - Raised for each test case below

    Return Value: N/A """
    # pylint: disable=unused-argument

    # email does not belong to a user
    # with pytest.raises(InputError):
    #     auth_login_v1('ghi@jkl.com', 'password')
    resp0 = requests.post(config.url + 'auth/login/v2', 
                          json={'email': 'ghi@jkl.com', 'password': 'password'})
    assert resp0.status_code == 400

    # incorrect password
    # with pytest.raises(InputError):
    #     auth_login_v1('abc@def.com', 'wordpass')
    resp1 = requests.post(config.url + 'auth/login/v2', 
                          json={'email': 'abc@def.com', 'password': 'wordpass'})
    assert resp1.status_code == 400

# clear_v1()
requests.delete(config.url + 'clear/v1')
