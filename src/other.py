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
import jwt, datetime

TOKEN_CODE = 'hotpot'
algorithm = 'HS256'
SESSION_ID_COUNTER = 0

def clear_v1():
    """
    clears the stored data in data_store

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    data_store.set(store)

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

    if isinstance(channel_id, int) is False or type(channel_id) is bool:
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
    """
    checks if the given user is a member of the given channel by searching
    the stored channel member data

    Arguments:
        auth_user_id (int) - a int that represents a user
        channel_id (int) - a int that represents a channel

    Exceptions: N/A

    Return Value:
        Returns a Boolean depending on if the auth_user_id is found in the
        channel members data
    """

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    return True

    return False



# called when a user logs in and registers.
def token_generate(user_data):
    global SESSION_ID_COUNTER # needed to pull the variable, not re-declare it, allows for modification, not needed for reading.
    token = jwt.encode({'id': user_data['id'], 'session_id': SESSION_ID_COUNTER, 'handle': user_data['handle'], 'time': datetime.datetime.now()}, TOKEN_CODE, algorithm=algorithm)
    
    token_dict = {
        'user_id': user_data['id'],
        'session_id': SESSION_ID_COUNTER,
        'token': token,
        'time': datetime.datetime.now(),
    }
    store = data_store.get()
    store['tokens'].append(token_dict)
    data_store.set(store)
    SESSION_ID_COUNTER = SESSION_ID_COUNTER + 1
    return token_dict

# given a token, returns the user_id
def token_get_user_id(token):
    decoded = jwt.decode(token, TOKEN_CODE, algorithm)
    return int(decoded['user_id'])

# given a token, returns True if the token is < 24 hours old, otherwise False.
def token_check_time_frame(token):
    decoded = jwt.decode(token, TOKEN_CODE, algorithm)
    token_lifetime = datetime.datetime.now() - decoded['time']
    if token_lifetime.days == 0:
        return True
    return False

# given a token, validate that the token exists in the tokens diction in data_store
def token_valid_check(token):
    store = data_store.get()
    for stored_token in store['token']:
        if token == stored_token:
            return True
    return False

# when the token is older then 24hr, remove from the datastore dict list.
def token_expired(token):
    return

