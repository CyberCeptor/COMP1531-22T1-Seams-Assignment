"""
Filename: user.py

Author: Jenson Morgan(z5360181), Xingjian Dong (z5221888)
Created: 22/02/2022 - 28/03/2022

Description:
    user.py contains the implementation for
    -   user_profile_v1: return the user information from a token and u_id.
    -   user_setemail_v1: set a new email for the user, in users, and the
        channels the user is in
    -   user_setname_v1: set the user's first name and last name, in the user
        and channels data_store
    - user_set_handle_v1: set the user's handle with the new information
        Helper Function: 
            - check_valid_handle: checks the handle is authentic
"""

from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id, cast_to_int_get_requests
from src.auth import check_invalid_email, check_invalid_name
from src.error import InputError

def user_profile_v1(token, u_id):
    """
    For a valid user, returns information about their user_id, firstname,
    last name, and handle

    Arguments:
        token (str) - a valid jwt token string
        u_id (int)  - an int specifying a user

    Exceptions: N/A

    Return: Returns a user's user_id, email, name_first, name_last, handle_str
    """

    token_valid_check(token)

    # cast u_id into an int since it is a GET request
    u_id = cast_to_int_get_requests(u_id, 'user id')

    check_valid_auth_id(u_id)

    store = data_store.get()
    # iterates through the users in data_store and collects
    # the information of that user.

    for users in store['users']:
        if users['id'] == u_id:
            user = {
                'u_id': users['id'],
                'email': users['email'],
                'name_first': users['first'],
                'name_last': users['last'],
                'handle_str': users['handle'],
            }

    return user

def user_profile_setemail_v1(token, email):
    """
    Update the authorised user's email
    
    Arguments:
        -   token
        -   email
    
    Exceptions:
        InputError: given email does not match the given valid email regex
    
    Return Value:
        N/A
    """

    store = data_store.get()

    # check the email is valid (i.e. usable email address, format)
    # check that the email isn't already used by another user
    # both done by check_invalid_email.

    token_valid_check(token)
    user_id = token_get_user_id(token)

    check_invalid_email(store, str(email))

    # set the user email to the new email
    for user in store['users']:
        if user['id'] == user_id:
            user['email'] = email

    # iterate through all channels that the member is in and set 
    # the email there aswell.

    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['email'] = email
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['email'] = email

    for dm in store['dms']:
        for user in dm['members']:
            if user['u_id'] == user_id:
                user['email'] = email

    data_store.set(store)
    return {}

def user_profile_setname_v1(token, name_first, name_last):
    """
    Update the authorised user's first and last name
    
    Arguments:
        -   token
        -   name_first
        -   name_last
    
    Exceptions:
        InputError:
            -   length of name_first is not between 1 and 50 characters inclusive
            -   length of name_last is not between 1 and 50 characters inclusive
    
    Return Value:
        N/A
    """
    store = data_store.get()

    # check the name is valid (i.e. usable name_first, name_last)
    # both done by check_invalid_name.
    # need to check that the name is the correct format.

    # check the token is current and acceptable
    token_valid_check(token)
    user_id = token_get_user_id(token)

    if type(name_first) is not str or type(name_first) is bool:
        raise InputError(description='Invalid first name')

    if type(name_last) is not str or type(name_last) is bool:
        raise InputError(description='Invalid last name')

    check_invalid_name(name_first, name_last)

    # set the user name to the new name
    for user in store['users']:
        if user['id'] == user_id:
            user['first'] = name_first
            user['last'] = name_last

    # iterate through all channels that the member is in and set 
    # the name there aswell.

    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['name_first'] = name_first
                user['name_last'] = name_last
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['name_first'] = name_first
                user['name_last'] = name_last

    for dm in store['dms']:
        for user in dm['members']:
            if user['u_id'] == user_id:
                user['name_first'] = name_first
                user['name_last'] = name_last

    data_store.set(store)
    return {}

def check_invalid_handle(store, handle_str):
    if type(handle_str) is not str or type(handle_str) is bool:
        raise InputError(description='Invalid handle_str')

    # check for invalid handle_str
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description='Invalid handle_str')
    
    # check for invalid handle_str
    if handle_str.isalnum() is False:
        raise InputError(description='Invalid handle_str')

    # check for duplicate handle_str
    for user in store['users']:
        if user['handle'] == handle_str and user['removed'] is False:
            raise InputError(description='Handle has already been taken')


def user_profile_sethandle_v1(token, handle_str):
    store = data_store.get()
    token_valid_check(token)
    user_id = token_get_user_id(token)

    check_invalid_handle(store, handle_str)

    for user in store['users']:
        if user['id'] == user_id:
            user['handle'] = handle_str

    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['handle_str'] = handle_str
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['handle_str'] = handle_str

    for dm in store['dms']:
        for user in dm['members']:
            if user['u_id'] == user_id:
                user['handle_str'] = handle_str

    data_store.set(store)
    return {}

