"""
Filename: other.py

Author: group
Created: 24/02/2022 - 27/03/2022

Description: implementation for
    - clearing all stored data in data_store
    - helper functions used over multiple files
        - checking if an auth_user_id is valid
        - checking if a channel_id is valid
        - checking if a user is a member of a channel or dm
        - checking if a user is a global owner
        - casting a variable into an int to check for invalid inputs for
          GET requests
        - getting messages from a channel or dm
        - sending a message to a channel or dm
        - checking if a dm id is valid
"""

from src.error import InputError

from src.data_store import data_store

from src.global_vars import reset_id, GLOBAL_OWNER

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
                    'handle_str': user['handle']
                }
            }

    # if the auth_user_id is not found, raise an InputError
    raise InputError(description='User does not exist in users database')

def check_valid_channel_id(channel_id):
    """
    checks if the given channel_id is valid by checking if it is larger than
    0 and if it is found in the stored channel data

    Arguments:
        channel_id (int) - a int that represents a channel

    Exceptions:
        InputError - Occurs if channel_id is not of type int, is less than 1 or
        is not found in the stored channel data

    Return Value:
        Returns the stored channel data if the channel_id is found
    """
    
    # bools are read as int's 0 & 1, so need to check prior
    if type(channel_id) is bool:
        raise InputError(description='Invalid channel_id type')

    # for GET requests since params are taken in as strings
    channel_id = cast_to_int_get_requests(channel_id, 'channel id')

    if channel_id < 1:
        raise InputError(description='The channel id is not valid')

    # if the channel_id is found, return the user data
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    # if the channel_id is not found, raise an InputError
    raise InputError(description='Channel does not exist in channels database')

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
        if user['id'] == auth_user_id and user['perm_id'] == GLOBAL_OWNER:
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
