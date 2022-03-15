"""
Filename: auth.py

Author: Aleesha, z5371516
Created: 24/02/2022 - 04/03/2022

Description: implementation for
    - registering a user using an email, password, first name, and last name
    - using an email and password to login to a user's account
    - helper functions for the above
"""

import re

from src.error import InputError

from src.data_store import data_store

VALID_EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

def auth_login_v1(email, password):
    """
    logs a user in with the given email and password and returns their
    authorised user id

    Arguments:
        email (str)    - a string that matches the VALID_EMAIL_REGEX above
        password (str) - a string that can contain any characters

    Exceptions:
        InputError - Occurs if the email belongs to a valid user but the
        incorrect password is given, and if the given email does not belong to a
        valid user

    Return Value:
        Returns a dict containing the auth_user_id if the email and password
        combination is valid
    """

    store = data_store.get()
    u_id = -1

    # iterates through stored user data and checks if any emails and passwords
    # match the given ones
    for user in store['users']:
        stored_email = user['email']
        stored_pw = user['pw']
        if stored_email == email:
            # correct email and password
            if stored_pw == password:
                u_id = user['id']
            else: # email belongs to a user but incorrect password
                raise InputError('Incorrect password')

    # if u_id = -1 then a user with given email does not exist
    if u_id == -1:
        raise InputError('Email does not belong to a user')

    return {
        'auth_user_id': u_id,
    }

# based on code Haydon wrote in project starter video
def auth_register_v1(email, password, name_first, name_last):
    """
    registers a user with the given email, password, name_first and
    name_last and stores this information in data_store

    Arguments:
        email (str)      - a string that matches the VALID_EMAIL_REGEX above
        password (str)   - a string that can contain any characters
        name_first (str) - a string that can contain a-z, A-Z, -, ' and spaces
        name_last (str)  - a string that can contain a-z, A-Z, -, ' and spaces

    Exceptions:
        InputError - Occurs if the password is less than 6 letters

    Return Value:
        Returns a dict containing the generated auth_user_id
    """

    store = data_store.get()
    # generate user id
    u_id = len(store['users']) + 1

    check_invalid_email(store, VALID_EMAIL_REGEX, email)

    # check for invalid password
    if len(password) < 6:
        raise InputError('Password is too short')

    # check for invalid name
    full_name = name_first + name_last
    check_invalid_name(name_first, name_last, full_name)

    handle = create_handle(store, full_name)

    # append user data as a dictionary if everything is valid
    user_dict = {
        'id': u_id,
        'email': email,
        'pw': password,
        'first': name_first,
        'last': name_last,
        'handle': handle,
        'perm_id': 1 if u_id == 1 else 2
    }

    # store the user information into the list of users
    store['users'].append(user_dict)
    data_store.set(store)

    return {
        'auth_user_id': u_id,
    }

def check_invalid_email(store, valid_email_regex, email):
    """
    tests if the given email is valid using the VALID_EMAIL_REGEX and checks
    if there is already another user with that email

    Arguments:
        store (dict) - a dict that stores user and channel data
        valid_email_regex (regex) - a string that can contain any characters
        email (str)  - a string that matches the VALID_EMAIL_REGEX above

    Exceptions:
        InputError - Occurs if the email doesn't match the regex and if there is
        already a user with the same email

    Return Value: N/A
    """

    # check for valid email address
    if not re.fullmatch(valid_email_regex, email):
        raise InputError('Invalid email address')

    # check for duplicate email
    for user in store['users']:
        if user['email'] == email:
            raise InputError('Email has already been taken')

def check_invalid_name(name_first, name_last, full_name):
    """
    tests if the given name is valid using the VALID_NAME_REGEX above and
    checks if the names will create an invalid handle

    Arguments:
        name_first (str) - a string that contains the user's first name
        name_last (str)  - a string that contains the user's last name
        full_name (str)  - a string that contains the user's first and last name

    Exceptions:
        InputError - Occurs if the first and/or last name doesn't match the
        VALID_NAME_REGEX, and if the fullname would create an invalid handle

    Return Value: N/A
    """

    # check for invalid first name
    if name_first == '' or len(name_first) > 50:
        raise InputError('Invalid first name')

    # check for invalid last name
    if name_last == '' or len(name_last) > 50:
        raise InputError('Invalid last name')

    # check for invalid full name
    count_alpha = 0
    for char in full_name:
        if char.isalpha() is True:
            count_alpha += 1
    if count_alpha == 0:
        raise InputError('Invalid name')

def create_handle(store, full_name):
    """
    creates the user's handle from their full name

    Arguments:
        store (dict)    - a dict that stores user and channel data
        full_name (str) - a string that contains the user's first and last name

    Exceptions: N/A

    Return Value:
        Returns a string containing the generated handle
    """

    # create a handle by removing any valid name symbols and lowering the case
    handle = ''.join(char for char in full_name if char.isalnum())
    handle = handle.lower()

    # slice the handle if it is too long
    if len(handle) > 20:
        handle = handle[0:20]

    # iterates through stored handles and checks for duplicates
    duplicate_count = -1
    for user in store['users']:
        to_compare = user['handle']
        if to_compare[-1].isnumeric() is True:
            if to_compare.rstrip(to_compare[-1]) == handle:
                duplicate_count += 1
        elif to_compare == handle:
            duplicate_count += 1

    # if there are duplicates, add the corresponding number to the end of
    # the handle, starts from 0
    if duplicate_count > -1:
        handle = handle + str(duplicate_count)

    return handle
