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

from src.data_store import data_store

def clear_v1():
    """ clears the stored data in data_store

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    data_store.set(store)

def check_valid_auth_id(auth_user_id):
    """ checks if the given auth_user_id is valid by checking if it is larger
    than 0 and if it is found in the stored user data

    Arguments:
        auth_user_id (int) - a int that represents a user

    Exceptions:
        InputError - Occurs if auth_user_id is not of type int
        AccessError - Occurs if auth_user_id is less than 1 or is not found
        in the stored user data

    Return Value: N/A """

    if isinstance(auth_user_id, int) is False:
        raise InputError('User id is not of a valid type')

    if auth_user_id < 1:
        raise AccessError('The user id is not valid (out of bounds)')

    store = data_store.get()
    user_exists = False
    for user in store['users']:
        if user['id'] == auth_user_id:
            user_exists = True

    # if the auth_user_id is not found, raise an AccessError
    if user_exists is False:
        raise AccessError('User does not exist in users database')

def check_valid_channel_id(channel_id):
    """ checks if the given channel_id is valid by checking if it is larger than
    0 and if it is found in the stored channel data

    Arguments:
        channel_id (int) - a int that represents a channel

    Exceptions:
        InputError - Occurs if channel_id is not of type int, is less than 1 or
        is not found in the stored channel data

    Return Value: N/A """

    if isinstance(channel_id, int) is False:
        raise InputError('Channel id is not of a valid type')

    if channel_id < 1:
        raise InputError('The channel id is not valid (out of bounds)')

    store = data_store.get()
    channel_exists = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel_exists = True

    # if the auth_user_id is not found, raise an AccessError
    if channel_exists is False:
        raise InputError('Channel does not exist in channels database')

def check_user_is_member(auth_user_id, channel_id):
    """ checks if the given user is a member of the given channel by searching
    the stored channel member data

    Arguments:
        auth_user_id (int) - a int that represents a user
        channel_id (int) - a int that represents a channel

    Exceptions: N/A

    Return Value:
        Returns a Boolean depending on if the auth_user_id is found in the
        channel members data """

    store = data_store.get()
    channel = store['channels'][channel_id - 1]
    if auth_user_id in channel['all_members']:
        return True

    return False
