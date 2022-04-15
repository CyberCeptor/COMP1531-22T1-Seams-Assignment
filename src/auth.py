"""
Filename: auth.py

Author: Aleesha Bunrith(z5371516), Jenson Morgan(z5360181)
Created: 24/02/2022 - 27/03/2022

Description: implementation for
    - registering a user using an email, password, first name, and last name
    - using an email and password to login to a user's account
    - logging out a user with their current valid token
    - generating a reset code to be sent in a password reset email
    - helper functions for the above
"""

import re

import hashlib

import random

import time

from src.error import InputError

from src.token import token_generate, token_remove

from src.data_store import data_store

from src.global_vars import Permission


MAX_NUM_CODES = 10**6
# The default image for user's when they register.
img_url = 'https://tvtunesquiz.com/wp-content/uploads/pingu.jpg'

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

    check_invalid_password(password)

    # encrypt the given password for storage
    encrypted_pw = hashlib.sha256(password.encode()).hexdigest()

    # check for invalid name and return the full name
    full_name = check_invalid_name(name_first, name_last)

    handle = create_handle(store, full_name)

    '''Get a default image.'''
    time_stamp = int(time.time())
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
        'profile_img_url': 'src/static/default.jpg',
        'reset_code': None,
        'user_stats': {
            'channels_joined': [{'num_channels_joined': 0, 'time_stamp': time_stamp}],
            'dms_joined': [{'num_dms_joined': 0, 'time_stamp': time_stamp}],
            'messages_sent': [{'num_messages_sent': 0, 'time_stamp': time_stamp}],
            'involvement_rate': 0,
        }
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

def check_invalid_password(password):
    """
    tests if the given password is valid

    Arguments:
        password (str) - a password given by the user

    Exceptions:
        InputError - Occurs if the password is less than 6 characters long or is 
                     of the wrong input type

    Return Value: N/A
    """

    if isinstance(password, str) is False:
        raise InputError(description='Password is not of a valid type')

    # check password length
    if len(password) < 6:
        raise InputError(description='Password is too short')

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

def generate_reset_code(email):
    """
    Generates a 6 digit code string to be sent in a password reset email if the
    given email belongs to a current user

    Arguments:
        email (str) - a address given by the user to send a reset email to

    Exceptions: N/A

    Return: 
        Returns the generated code if the email belongs to a user. Otherwise, 
        returns None
    """

    store = data_store.get()

    user_data = None

    # find email in stored user data and return the user's data
    for user in store['users']:
        if user['email'] == email and user['removed'] is False:
            user_data = user
    
    # if email is not found in data, no errors are raised and return None
    if user_data is None:
        return None
    
    # if email is found, generate a random 6 digit code string and return it so
    # it can be used to send the password reset email
    code = f'{random.randrange(0, 10**6):06}'

    # if code has been generated before, generate a new one
    while code in [user['reset_code'] for user in store['users']]:
        code = f'{random.randrange(0, 10**6):06}'

    # the reset code stored in the user data will be updated so only the code 
    # that is sent the latest is valid (if the user request multiple times)
    user_data['reset_code'] = code

    # log the user out by removing any current tokens
    for token_data in store['tokens']:
        if token_data['user_id'] == user_data['id']:
            token_remove(token_data['token'])

    data_store.set(store)

    return code

def passwordreset_reset_v1(reset_code, new_password):
    """
    Given a reset_code and new_password, reset the user's password whom the 
    reset_code belongs to

    Arguments:
        reset_code (str)   - a unique str that belongs to a user to reset a pw
        new_password (str) - the new pw the user wants to use for their acc

    Exceptions: 
        InputError - Raised if reset_code is invalid or new_passord is invalid

    Return: N/A
    """

    store = data_store.get()

    # if input is None, it will be considered a valid code
    if reset_code is None:
        raise InputError(description='Invalid reset code')

    user = get_user_with_reset_code(reset_code)

    check_invalid_password(new_password)

    # reset the user's new encrypted password
    user['pw'] = hashlib.sha256(new_password.encode()).hexdigest()

    user['reset_code'] = None

    data_store.set(store)

def get_user_with_reset_code(reset_code):
    """
    Checks whether the given reset_code belongs to a user and returns that 
    user's data

    Arguments:
        reset_code (str) - a unique str that belongs to a user to reset a pw

    Exceptions: 
        InputError - Raised if reset_code is not store in any user data

    Return: Returns the user that holds the given reset_code
    """

    store = data_store.get()

    # find the user which the reset code belongs to, also doubles as a valid 
    # input check
    for user in store['users']:
        if user['reset_code'] == reset_code:
            return user
    
    raise InputError(description='Invalid reset code')
