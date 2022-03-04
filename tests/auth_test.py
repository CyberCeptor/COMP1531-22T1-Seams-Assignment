"""
Filename: auth_test.py

Author: Aleesha, z5371516
Created: 24/02/2022 - 04/03/2022

Description: pytests for auth_register_v1 and auth_login_v1
"""

import pytest

from src.auth import auth_login_v1, auth_register_v1

from src.other import clear_v1
from src.error import InputError

from src.data_store import data_store

NAME_22_CHARS = 'abcdefghijklmnopqrstuv'
NAME_52_CHARS = 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz'

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """ clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')

@pytest.fixture(name='stored_data')
def fixture_get_stored_data():
    """ clears any data stored in data_store and returns the users dict

    Arguments: N/A

    Exceptions: N/A

    Return Value:
        Returns the users dict from data_store """

    clear_v1()
    store = data_store.get()
    users = store['users']
    return users

def test_register_invalid_email():
    """ registers a user with an invalid email and raises an InputError for each
    case

    Arguments: N/A

    Exceptions:
        InputError - Raised for all test cases listed below

    Return Value: N/A """

    # missing @ and .
    with pytest.raises(InputError):
        auth_register_v1('abc', 'password', 'first', 'last')

    # missing @
    with pytest.raises(InputError):
        auth_register_v1('abc.def', 'password', 'first', 'last')

    # missing .
    with pytest.raises(InputError):
        auth_register_v1('abc@def', 'password', 'first', 'last')

    # missing characters before @
    with pytest.raises(InputError):
        auth_register_v1('@def.com', 'password', 'first', 'last')

    # missing characters between @ and .
    with pytest.raises(InputError):
        auth_register_v1('abc@.com', 'password', 'first', 'last')

    # missing characters after .
    with pytest.raises(InputError):
        auth_register_v1('abc@def.', 'password', 'first', 'last')

    # numbers after .
    with pytest.raises(InputError):
        auth_register_v1('abc@def.123', 'password', 'first', 'last')

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

    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last')
    clear_v1()

def test_register_invalid_password():
    """ registers a user with an invalid password i.e one that is too short and
    raises an InputError

    Arguments: N/A

    Exceptions:
        InputError - Raised for the test case below

    Return Value: N/A """

    # password too short
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'pass', 'first', 'last')

def test_register_invalid_name():
    """ registers a user with an invalid name and raises an InputError for each
    case

    Arguments: N/A

    Exceptions:
        InputError - Raised for each test case below

    Return Value: N/A """

    # first name too short
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', '', 'last')

    # last name too short
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', '')

    # first name too long
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', NAME_52_CHARS, 'last')

    # last name too long
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', NAME_52_CHARS)

    # first name has symbols other than - and ' and spaces
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first@', 'last')

    # first name has numbers
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first1', 'last')

    # last name has symbols other than - and ' and spaces
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last@')

    # last name has numbers
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last1')

    # name has no letters -> would create an empty handle
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', '-', ' ')

# based on code Hayden wrote in project starter video
def test_register_works():
    """ tests if auth_register_v1 works by registering a user and logging them
    in

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    clear_v1()
    register_return = auth_register_v1('abc@def.com', 'password',
                                       'first', 'last')
    auth_user_id1 = register_return['auth_user_id']

    login_return = auth_login_v1('abc@def.com', 'password')
    auth_user_id2 = login_return['auth_user_id']

    # if user_id's are identical, then it is a vald login
    assert auth_user_id1 == auth_user_id2
    clear_v1()

def test_create_handle_invalid_symbols(stored_data):
    """ creates handles for the given users and tests if the valid name symbols
    are succesfully removed

    Arguments:
        stored_data (fixture) - returns the user dict from data_store

    Exceptions: N/A

    Return Value: N/A """

    # first name has symbols
    auth_register_v1('abc@def.com', 'password', "f'irst-fir st", 'last')
    handle0 = stored_data[0]['handle']
    assert handle0 == 'firstfirstlast'

    # last name has symbols
    auth_register_v1('abc@def.co', 'password', 'first', "la'st-la st")
    handle1 = stored_data[1]['handle']
    assert handle1 == 'firstlastlast'
    clear_v1()

def test_create_handle_capitals(stored_data):
    """ creates handles for the below users and tests if capitals are
    succesfully removed

    Arguments:
        stored_data (fixture) - returns the user dict from data_store

    Exceptions: N/A

    Return Value: N/A """

    # first name has capitals
    auth_register_v1('abc@def.com', 'password', 'FIRST', 'last')
    handle0 = stored_data[0]['handle']
    assert handle0 == 'firstlast'

    # last name has capitals
    auth_register_v1('abc@def.co', 'password', 'first', 'LASTY')
    handle1 = stored_data[1]['handle']
    assert handle1 == 'firstlasty'

    # both names have capitals
    auth_register_v1('abc@de.co', 'password', 'firST', 'LAStee')
    handle2 = stored_data[2]['handle']
    assert handle2 == 'firstlastee'
    clear_v1()

def test_create_handle_invalid_length(stored_data):
    """ creates handles for the below users and tests if extra characters are
    succesfully removed

    Arguments: N/A

    Exceptions:
        stored_data (fixture) - returns the user dict from data_store

    Return Value: N/A """

    # first name longer than 20 characters
    auth_register_v1('abc@def.com', 'password', NAME_22_CHARS, 'last')
    handle0 = stored_data[0]['handle']
    assert handle0 == 'abcdefghijklmnopqrst'

    # last name longer than 20 characters
    auth_register_v1('abc@def.co', 'password', 'first', NAME_22_CHARS)
    handle1 = stored_data[1]['handle']
    assert handle1 == 'firstabcdefghijklmno'

    # name longer than 20 characters
    auth_register_v1('abc@de.com', 'password', 'abcdefghijklmnopqr', 'last')
    handle2 = stored_data[2]['handle']
    assert handle2 == 'abcdefghijklmnopqrla'
    clear_v1()

def test_create_handle_duplicates(stored_data):
    """ creates handles for the below users and tests if duplicate handles are
    dealt with by adding on numbers

    Arguments: N/A

    Exceptions:
        stored_data (fixture) - returns the user dict from data_store

    Return Value: N/A """

    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    handle0 = stored_data[0]['handle']
    assert handle0 == 'firstlast'

    auth_register_v1('abc@def.co', 'password', 'first', 'last')
    handle1 = stored_data[1]['handle']
    assert handle1 == 'firstlast0'
    clear_v1()

def test_create_handle_invalid_length_duplicates(stored_data):
    """ creates handles for the below users and tests if extra characters are
    succesfully removed and if duplicate handles are dealt with by adding on
    numbers

    Arguments: N/A

    Exceptions:
        stored_data (fixture) - returns the user dict from data_store

    Return Value: N/A """

    auth_register_v1('abc@def.com', 'password', 'abcdefghijklmnopqr', 'last')
    handle0 = stored_data[0]['handle']
    assert handle0 == 'abcdefghijklmnopqrla'

    auth_register_v1('abc@def.co', 'password', 'abcdefghijklmnopqr', 'last')
    handle1 = stored_data[1]['handle']
    assert handle1 == 'abcdefghijklmnopqrla0'

    assert len(handle0) != len(handle1)

def test_login_invalid(clear_and_register):
    """ logs a user in and raises an InputError for each invalid case

    Arguments:
        clear_and_register (fixture)

    Exceptions:
        InputError - Raised for each test case below

    Return Value: N/A """
    # pylint: disable=unused-argument

    # email does not belong to a user
    with pytest.raises(InputError):
        auth_login_v1('ghi@jkl.com', 'password')

    # incorrect password
    with pytest.raises(InputError):
        auth_login_v1('abc@def.com', 'wordpass')

clear_v1()
