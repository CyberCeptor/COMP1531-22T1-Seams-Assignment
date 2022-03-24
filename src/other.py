"""
Filename: other.py

Author: group
Created: 24/02/2022 - 04/03/2022

Description: implementation for
    - clearing all stored data in data_store
    - helper functions for channel.py and channels.py
        - checking if an auth_user_id is valid
        - checking if a channel_id is valid
        - checking if a user is a member of a channel
"""
from src.error import InputError, AccessError

from src.token import reset_session_id

from src.data_store import data_store


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
    data_store.set(store)
    reset_session_id()

def check_valid_auth_id(auth_user_id):
    """
    checks if the given auth_user_id is valid by checking if it is larger
    than 0 and if it is found in the stored user data

    Arguments:
        auth_user_id (int) - a int that represents a user

    Exceptions:
        InputError - Occurs if auth_user_id is not of type int
        AccessError - Occurs if auth_user_id is less than 1 or is not found
        in the stored user data

    Return Value: N/A
    """

    if isinstance(auth_user_id, int) is False or type(auth_user_id) is bool:
        raise InputError('User id is not of a valid type')

    if auth_user_id < 1:
        raise InputError('The user id is not valid (out of bounds)')

    store = data_store.get()
    user_exists = False
    for user in store['users']:
        if user['id'] == auth_user_id:
            user_exists = True

    # if the auth_user_id is not found, raise an AccessError
    if user_exists is False:
        raise AccessError('User does not exist in users database')

def check_valid_channel_id(channel_id):
    """
    checks if the given channel_id is valid by checking if it is larger than
    0 and if it is found in the stored channel data

    Arguments:
        channel_id (int) - a int that represents a channel

    Exceptions:
        InputError - Occurs if channel_id is not of type int, is less than 1 or
        is not found in the stored channel data

    Return Value: N/A
    """
    '''Bools are read as int's 0 & 1, so need to check prior. (Not for GET requests)'''
    '''GET requests are read as a string.'''
    if type(channel_id) == bool:
        raise InputError('Invalid channel_id type')

    '''For GET requests.'''
    if channel_id in ['', 'True', 'False']:
        raise InputError('Invalid channel_id')
    try:
        channel_id = int(channel_id)
    except ValueError:
        raise InputError('Invalid channel id type') from InputError

    if channel_id < 1:
        raise InputError('The channel id is not valid (out of bounds)')

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    raise InputError('Channel does not exist in channels database')


def check_user_is_member(auth_user_id, channel_id):
    """
    checks if the given user is a member of the given channel by searching
    the stored channel member data

    Arguments:
        auth_user_id (int) - a int that represents a user
        channel_id (int) - a int that represents a channel

    Exceptions: N/A

    Return Value:
        Returns a the channel member data if the auth_user_id is found in the
        channel. Otherwise returns None
    """

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    return member

    return None

def check_user_is_owner_member(auth_user_id, channel_id):
    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['owner_members']:
                if member['u_id'] == auth_user_id:
                    return member
    return None

def check_user_is_global_owner(auth_user_id):
    """
    check the user whether is a global owner with auth user id

    Arguments:
        auth_user_id (int) - an integer that specifies user id

    Exceptions: N/A

    Return Value: True if the user is a global owner, False otherwise
    """

    store = data_store.get()
    for user in store['users']:
        if user['id'] == auth_user_id and user['perm_id'] == 1:
            return True
    return False
