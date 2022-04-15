"""
Filename: other.py

Author: group
Created: 24/02/2022 - 13/04/2022

Description: implementation for
    - clearing all stored data in data_store
    - helper functions used over multiple files
        - checking if an auth_user_id is valid
        - checking if a channel_id is valid
        - checking if a user is a member of a channel or dm
        - checking if a user is a global owner
        - casting a variable into an int to check for invalid inputs for
          GET requests
"""

import os

import glob

from src.error import InputError

from src.data_store import data_store

from src.global_vars import reset_id, Permission

def clear_v1():
    """
    clears the stored data in data_store

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    store = data_store.get()
    store['users'].clear()
    store['channels'].clear()
    store['tokens'].clear()
    store['dms'].clear()

    images = glob.glob('src/static/*')
    for pic in images:
        if pic != 'src/static/default.jpg':
            os.remove(pic)

    data_store.set(store)
    
    reset_id('session')
    reset_id('message')
    reset_id('dm')
    
def check_valid_auth_id(auth_user_id):
    """
    checks if the given auth_user_id is valid by checking if it is of valid
    input, larger than 1, and if it is found in the stored user data

    Arguments:
        auth_user_id (int) - a int that represents a user

    Exceptions:
        InputError - Occurs if auth_user_id is not of type int
        AccessError - Occurs if auth_user_id is less than 1 or is not found
        in the stored user data

    Return Value:
        Returns the stored user data if the auth_user_id is found
    """
    
    if isinstance(auth_user_id, int) is False or type(auth_user_id) is bool:
        raise InputError(description='User id is not of a valid type')

    if auth_user_id < 1:
        raise InputError(description='The user id is not valid')

    # if the auth_user_id is found, return the user data
    store = data_store.get()
    for user in store['users']:
        if user['id'] == auth_user_id:
            return {
                'all_data': user, 
                'return_data': {
                    'u_id': user['id'],
                    'email': user['email'],
                    'name_first': user['first'],
                    'name_last': user['last'],
                    'handle_str': user['handle'],
                    'profile_img_url': user['profile_img_url'],
                }
            }

    # if the auth_user_id is not found, raise an InputError
    raise InputError(description='User does not exist in users database')

def check_valid_dm_channel_id(data_id, option, share):
    """
    checks if the given id is valid

    Arguments:
        data_id (int) - a int that represents a channel or dm
        option (str)  - denotes if the id channel or dm
        share (bool)  - indicates if the id is being checked from message/share

    Exceptions:
        InputError - Occurs if id is not of type int, is less than 1
        (if share is False) or is not found in the stored channel data

    Return Value:
        Returns the stored channel or dm data if the id is found
    """

    if option == 'channel':
        dict_key = 'channels'
        id_key = 'channel_id'
    else: # option == 'dm'
        dict_key = 'dms'
        id_key = 'dm_id'

    if type(data_id) is bool:
        raise InputError(f'{option} id is not of a valid type')

    # cast dm_id to an int since it is a GET request
    data_id = cast_to_int_get_requests(data_id, f'{option} id')

    if data_id < 1 and share is False:
        raise InputError(f'The {option} id is not valid (out of bounds)')

    # id -1 is only valid is share is True
    if data_id == -1 and share is True:
        return

    store = data_store.get()
    for data in store[dict_key]:
       if data[id_key] == data_id:
            return data

    # if the data_id is not found, raise an AccessError
    raise InputError(f'{option} does not exist in data')

def check_user_is_member(auth_user_id, data, key):
    """
    checks if the given user is a member of the given channel by searching
    the stored channel member data

    Arguments:
        auth_user_id (int) - a int that represents a user
        data (data)        - a dict storing the channel or dm info
        key (str)          - a string that is used to access member data for
                             the given data
                               - 'all_members' or 'owner_members' for channels
                               - 'members' for dms

    Exceptions: N/A

    Return Value:
        Returns a the channel member data if the auth_user_id is found in the
        channel. Otherwise returns None
    """

    for member in data[key]:
        if member['u_id'] == auth_user_id:
            return member
    return None

def check_user_is_global_owner(auth_user_id):
    """
    check the user whether is a global owner with auth user id

    Arguments:
        auth_user_id (int) - an integer that specifies a user

    Exceptions: N/A

    Return Value:
        True if the user is a global owner, False otherwise
    """

    store = data_store.get()
    for user in store['users']:
        if user['id'] == auth_user_id and user['perm_id'] == Permission.OWNER.value:
            return True
    return False

def cast_to_int_get_requests(variable, var_name):
    """
    casts the given variable from a get request into an int

    Arguments:
        variable (any type) - a variable to be cast to an int
        var_name (str)      - a string used to print out any error messages if
                              InputError is raised
    Exceptions:
        InputError - Raised if the variable can't be turned into an int

    Return Value:
        Returns the variable casted to an int if there are no errors raised
    """

    # tries to cast the given variable to an int, raise an InputError if an
    # ValueError is given
    try:
        variable = int(variable)
    except ValueError:
        raise InputError(description=f'Invalid {var_name}') from InputError

    return variable


