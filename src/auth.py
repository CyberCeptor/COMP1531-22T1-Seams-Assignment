"""
Filename: auth.py

Author: Aleesha Bunrith(z5371516), Jenson Morgan(z5360181)
Created: 24/02/2022 - 27/03/2022

Description: implementation for
    - registering a user using an email, password, first name, and last name
    - using an email and password to login to a user's account
    - logging out a user with their current valid token
    - helper functions for the above
"""

import re

import hashlib

from src.error import InputError

from src.data_store import data_store
from src.token import token_generate

from src.global_vars import Permission

def auth_login_v2(email, password):
    """
    logs a user in with the given email and password and returns their
    authorised user id

    Arguments:
        email (str)    - a string that matches the valid_email_regex above
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
    token = -1

    # iterates through stored user data and checks if any emails and passwords
    # match the given ones
    for user in store['users']:
        stored_email = user['email']
        stored_pw = user['pw']
        if stored_email == email:
            # correct email and password
            encrypted_pw = hashlib.sha256(password.encode()).hexdigest()
            if stored_pw == encrypted_pw:
                u_id = user['id']
                token = token_generate(user)
            else: # email belongs to a user but incorrect password
                raise InputError(description='Incorrect password')

    # if u_id = -1 then a user with given email does not exist
    if u_id == -1:
        raise InputError(description='Email does not belong to a user')

    return {
        'token': token,
        'auth_user_id': u_id,
    }

# based on code Haydon wrote in project starter video
def auth_register_v2(email, password, name_first, name_last):
    """
    registers a user with the given email, password, name_first and
    name_last and stores this information in data_store

    Arguments:
        email (str)      - a string that matches the valid_email_regex
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

    check_invalid_email(store, email)

    # check for invalid password
    if len(password) < 6:
        raise InputError(description='Password is too short')

    # encrypt the given password for storage
    encrypted_pw = hashlib.sha256(password.encode()).hexdigest()

    # check for invalid name and return the full name
    full_name = check_invalid_name(name_first, name_last)

    handle = create_handle(store, full_name)

    # append user data as a dictionary if everything is valid
    user_dict = {
        'id': u_id,
        'email': email,
        'pw': encrypted_pw,
        'first': name_first,
        'last': name_last,
        'handle': handle,
        'notifications': [],
        'perm_id': Permission.OWNER.value if u_id == 1 else Permission.USER.value,
        'removed': False,
        'profile_img_url': None,
    }

    # store the user information into the list of users
    store['users'].append(user_dict)
    data_store.set(store)

    return {
        'token': token_generate(user_dict),
        'auth_user_id': u_id,
    }

def check_invalid_email(store, email):
    """
    tests if the given email is valid using the valid_email_regex and checks
    if there is already another user with that email

    Arguments:
        store (dict) - a dict that stores user and channel data
        valid_email_regex (regex) - a string that can contain any characters
        email (str)  - a string that matches the valid_email_regex above

    Exceptions:
        InputError - Occurs if the email doesn't match the regex and if there is
        already a user with the same email

    Return Value: N/A
    """

    # valid email regex from spec
    valid_email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    # check for valid email address
    if not re.fullmatch(valid_email_regex, str(email)):
        raise InputError(description='Invalid email address')

    # check for duplicate email
    for user in store['users']:
        if user['email'] == email and user['removed'] is False:
            raise InputError(description='Email has already been taken')

def check_invalid_name(name_first, name_last):
    """
    tests if the given name is valid using the VALID_NAME_REGEX above and
    checks if the names will create an invalid handle

    Arguments:
        name_first (str) - a string that contains the user's first name
        name_last (str)  - a string that contains the user's last name
        full_name (str)  - a string that contains the user's first and last name

    Exceptions:
        InputError - Occurs if the first and/or last name is of an invalid type
                     and/or length
                   - Occurs if the user's names (concatenated) has less than one
                     alphnumeric character

    Return Value: N/A
    """

    # check for inputs of invalid type
    if type(name_first) is not str or type(name_first) is bool:
        raise InputError(description='Invalid first name')

    if type(name_last) is not str or type(name_last) is bool:
        raise InputError(description='Invalid last name')

    # check for invalid first name
    if name_first == '' or len(name_first) > 50:
        raise InputError(description='Invalid first name')

    # check for invalid last name
    if name_last == '' or len(name_last) > 50:
        raise InputError(description='Invalid last name')

    full_name = name_first + name_last

    # check for invalid full name
    count_alpha = 0
    for char in full_name:
        if char.isalpha() is True:
            count_alpha += 1
    if count_alpha == 0:
        raise InputError(description='Invalid name')
    
    return full_name

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
        if user['removed'] is False:
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
    