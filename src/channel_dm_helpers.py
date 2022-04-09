"""
Filename: channel_dm_helpers.py

Author: group
Created: 24/02/2022 - 27/03/2022

Description: implementation for
    - clearing all stored data in data_store
    - helper functions used over multiple files
        - getting messages from a channel or dm
        - sending a message to a channel or dm
        - checking if a dm id is valid
        - leaving a channel or dm
        - setting the is_this_user_reacted value
"""

import datetime

from datetime import timezone

from src.dm import dm_leave_v1

from src.error import InputError, AccessError
from src.other import check_user_is_member, check_valid_channel_id
from src.token import token_get_user_id, token_valid_check

from src.channel import channel_leave_v1

from src.data_store import data_store

from src.global_vars import new_id

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
    if data_str == 'channel':
        key = 'all_members'
    elif data_str == 'dm':
        key = 'members'

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
            set_is_this_user_reacted(auth_user_id, data['messages'], start, 
                                     start + 1)
            to_return.append(data['messages'][start])
        else:
            # if there are less than 50 messages from the index start or
            # if there are only 50 messages
            set_is_this_user_reacted(auth_user_id, data['messages'], start, 
                                     total_messages)
            to_return = [data['messages'][index] for index in
                         range(start, total_messages)]
    else:
        set_is_this_user_reacted(auth_user_id, data['messages'], start, end)
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
        AccessError - Raised if the user is not a member of the channel or dm
        InputError  - Raised if message is not of a valid type or length

    Return Value:
        Message_id - int to specifies each message
    """

    store = data_store.get()

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
        'time_sent': int(utc_timestamp),
        'reacts': [{
            'react_id': 1,
            'u_ids': [],
            'is_this_user_reacted': False,
        }],
        'is_pinned': False
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

def set_is_this_user_reacted(auth_user_id, messages, start, end):
    """
    sets the is_this_user_reacted to True or False for the given range of 
    messages data

    Arguments:
        auth_user_id (int) - the user id of the user that is requesting the 
                             channel or dm messages
        messages (dict)    - data of a channel or dm
        start (int)        - an int specifying the start index
        end (int)          - an int specifying the end index

    Exceptions: N/A

    Return Value: N/A
    """

    # loop through and set the is_this_user_reacted to the appropriate value
    for index in range(start, end):
        for react in messages[index]['reacts']:
            if auth_user_id in react['u_ids']:
                react['is_this_user_reacted'] = True
            else:
                react['is_this_user_reacted'] = False

@token_valid_check
def leave_channel_dm(token, data_id, option):
    """
    checks the given token, gets the user's id, and calls the dm_leave_v1 or
    channel_leave_v1 function depending on the option

    Arguments: token (str)   - a valid jwt token str
               data_id (int) - the given channel or dm id
               option (str)  - a str denoting whether the user is leaving a dm
                               or channel

    Exceptions: N/A

    Return Value: N/A
    """

    auth_user_id = token_get_user_id(token)

    if option == 'dm':
        dm_leave_v1(auth_user_id, data_id)
    elif option == 'channel':
        channel_leave_v1(auth_user_id, data_id)
