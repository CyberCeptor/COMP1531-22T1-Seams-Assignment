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
<<<<<<< HEAD

=======
>>>>>>> master
from src.error import InputError, AccessError
from src.token import reset_session_id
from src.data_store import data_store
from src.global_vars import reset_message_id
from src.global_vars import reset_dm_id

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
    reset_session_id()
    reset_message_id()
    reset_dm_id()
    
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
    for user in store['users']:
        if user['id'] == auth_user_id:
            return user

    # if the auth_user_id is not found, raise an InputError
    raise InputError('User does not exist in users database')

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
    if type(channel_id) is bool:
        raise InputError('Invalid channel_id type')

    '''For GET requests.'''
    channel_id = cast_to_int_get_requests(channel_id, 'channel id')

    if channel_id < 1:
        raise InputError('The channel id is not valid (out of bounds)')

    store = data_store.get()
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel

    raise InputError('Channel does not exist in channels database')

def check_user_is_member(auth_user_id, data, key):
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

    for member in data[key]:
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
            
def get_channel_id_with_message_id(message_id):
    store = data_store.get()
    for channel in store['channels']:
        for message_data in channel['messages']:
            if message_data['message_id'] == message_id:
                return channel


def check_message_id_valid(message_id):
    """
    checks if the given message_id is valid by checking if it exists in stored data

    Arguments:
        message_id (int) - a int that represents a channel

    Exceptions:
        InputError - 
            raised for all cases below
    Return Value: N/A
    """

    if isinstance(message_id, int) is False or type(message_id) == bool:
        raise InputError('Message id is not of a valid type')

    if message_id < 1:
        raise InputError('The message id is not valid (out of bounds)')

    store = data_store.get()
    for channel in store['channels']:
        for message_data in channel['messages']:
            # check if message id exists
            if message_data['message_id'] == message_id:
                return message_data
            
    raise InputError('Message does not exist in channels database')

def cast_to_int_get_requests(variable, var_name):
    """
    casts the given variable from a get request into an int

    Arguments:
        variable (any type) - a variable to be cast to an int
        var_name (str)      - a string used to print out any error messages if
                              InputError is raised
    Exceptions:
        InputError - Raised if the variable can't be turned into an int

    Return Value: Returns the variable casted to an int
    """

    try:
        variable = int(variable)
    except ValueError:
        raise InputError(description=f'Invalid {var_name}') from InputError

    return variable

def get_messages(auth_user_id, data, start, data_str):
    if data_str == "channel":
        key = "all_members"
    elif data_str == "dm":
        key = "members"

    # is_member is a bool to check whether given user is in the given channel
    if check_user_is_member(auth_user_id, data, key) is None:
        raise AccessError(f'User does not exist in {data_str}')

    total_messages = len(data['messages'])

    start = cast_to_int_get_requests(start, 'start')

    if start < 0:
        raise InputError('Invalid start')
    elif start > total_messages:
        raise InputError('Invalid start, not enough messages')

    if total_messages == 0:
        return {
            'messages': [],
            'start': start,
            'end': -1,
        }

    # message starts
    start_message = data['messages'][start]

    # get end
    end = start + 50

    # make sure end is suitable index place
    if end >= total_messages:
        end = -1

    # the messages list
    messages_to_return = []

    # if mesages not overflow
    if end == -1:
        if start == total_messages - 1: # if there is only 1 message
            messages_to_return.append(start_message)
        else:
            for idx, message in data['messages']:
                if idx >= start:
                    messages_to_return.append(message)
    else:
        for idx, message in data['messages']:
            if start <= idx < end:
                messages_to_return.append(message)

    return {
        'messages': messages_to_return,
        'start': start,
        'end': end,
<<<<<<< HEAD
    }
=======
    }
>>>>>>> master
