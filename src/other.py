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

import datetime

from datetime import timezone

from src.error import InputError, AccessError
from src.token import token_valid_check, token_get_user_id

from src.data_store import data_store

from src.global_vars import new_id, reset_id

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
            return user

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
        if user['id'] == auth_user_id and user['perm_id'] == 1:
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

def get_messages(auth_user_id, data, start, data_str):
    """
    returns the message data in a channel or dm from index start to start + 50

    Arguments:
        auth_user_id (int) - an integer that specifies a user
        data (dict)        - a dict storing the channel or dm info
        start (int)        - an int specifying the start index for the return of
                             messages data
        data_str (str)     - a string used to print out any error messages if
                             InputError is raised and to check if messages are
                             being obtained from a channel or dm

    Exceptions:
        AccessError - Raised if the auth_user_id is not a member of the given
                      channel or dm
        InputError  - Raised if start is of an invalid type or input

    Return Value:
        Returns a dict of returned messages, start index, and end index
    """

    # grab the correct members key depending on if messages are being returned
    # from channel or dm data
    if data_str == "channel":
        key = "all_members"
    elif data_str == "dm":
        key = "members"

    # check whether given user is in the given channel
    if check_user_is_member(auth_user_id, data, key) is None:
        raise AccessError(description=f'User does not exist in {data_str}')

    total_messages = len(data['messages'])

    # check start is of valid input type and input
    start = cast_to_int_get_requests(start, 'start')

    if start < 0:
        raise InputError(description='Invalid start')
    elif start > total_messages:
        raise InputError(description='Invalid start, not enough messages')

    # return an empty messages list if there are no messages to get
    if total_messages == 0:
        return {
            'messages': [],
            'start': start,
            'end': -1,
        }

    # get end
    end = start + 50

    print(total_messages)

    # make sure end is suitable index place
    if end > total_messages:
        end = -1
    elif end == total_messages:
        end = -1

    # the messages list
    to_return = []

    if end == -1:
        if start == total_messages - 1:
            # if there is only 1 message
            to_return.append(data['messages'][start])
        else:
            # if there are less than 50 messages from the index start or
            # if there are only 50 messages
            to_return = [data['messages'][index] for index in
                         range(start, total_messages)]
    else:
        to_return = [data['messages'][index] for index in range(start, end)]

    return {
        'messages': to_return,
        'start': start,
        'end': end,
    }

def send_message(token, data_id, message, data_str):
    """
    Helper function for message/send and message/senddm: If token given is an
    authorised user, sends the message to a specified channel/dm with input
    data_id

    Arguments:
        token (str)    - unique str representation of user
        dm_id (int)    - integer specifies a dm or channel
        message (str)  - message that the user wishes to send
        data_str (str) - a string used to print out any error messages if
                         InputError is raised and to check if message is being
                         sent to a channel or dm

    Exceptions:
        AccessError - 
        InputError  - 

    Return Value:
        Message_id - int to specifies each message
    """

    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # check if dm_id/channel_id are valid
    if data_str == 'channel':
        data_info = check_valid_channel_id(data_id)
        data_id = data_info['channel_id']
        key = 'all_members'
    elif data_str == 'dm':
        data_info = check_valid_dm_id(data_id)
        data_id = data_info['dm_id']
        key = 'members'

    if check_user_is_member(auth_user_id, data_info, key) is None:
        raise AccessError(description=f'User does not exist in {data_str}')

    if not isinstance(message, str):
        raise InputError(description='Message is a string')

    if message == '':
        raise InputError(description='Empty message input')

    if len(message) > 1000:
        raise InputError(description='Message must not exceed 1000 characters')

    # increament message id for the store message
    message_id = new_id('message')

    # generate timestamp
    time = datetime.datetime.now(timezone.utc)
    utc_time = time.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    message_data = {
        'message_id': message_id, 
        'u_id': auth_user_id, 
        'message': message, 
        'time_sent': utc_timestamp
    }

    data_info['messages'].insert(0, message_data)

    data_store.set(store)

    return {
        'message_id': message_id
    }

def check_valid_dm_id(dm_id):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: token
               u_ids

    Exceptions: InputError - raised by duplicate ids
                InputError - raised by invalid ids

    Return Value: dm_id
    """

    if type(dm_id) is bool:
        raise InputError('dm id is not of a valid type')

    # cast dm_id to an int since it is a GET request
    dm_id = cast_to_int_get_requests(dm_id, 'dm id')

    if dm_id < 1:
        raise InputError('The dm id is not valid (out of bounds)')

    store = data_store.get()
    for dm in store['dms']:
       if dm['dm_id'] == dm_id:
            return dm

    # if the dm_id is not found, raise an AccessError
    raise InputError('dm does not exist in dms')
