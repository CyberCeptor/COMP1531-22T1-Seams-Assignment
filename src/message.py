"""
Filename: message.py

Author: Yangjun Yue(z5317840)
Created: 23/03/2022 - 27/03/2022

Description: implementation for
    - sending message to a specified channel by an authorised user
    - given a specified message id and editing that message
    - removing specified message from channel
"""

import datetime

from datetime import timezone

from src.dm import check_valid_dm_id

from src.admin import check_user_is_global_owner
from src.error import AccessError, InputError
from src.other import check_valid_auth_id, check_valid_channel_id,\
                      check_user_is_member
from src.token import token_get_user_id, token_valid_check

from src.data_store import data_store

from src.global_vars import new_id

def message_send_v1(token, channel_id, message):
    """
    If token given is authorised user, sends the message
    to a specified channel with input channel_id

    Arguments:
        token (str)          - unique str representation of user
        channel_id (int))    - integer sppcifies channel
        message (str)        - message that the user wishes to send

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - channel_id does not refer to valid channel
                    - length of message is less than 1 or over 1000 characters

    Return Value:
        Message_id - int to specifies each message
    """

    message_id = send_message(token, channel_id, message, 'channel')

    return message_id

def message_edit_v1(token, message_id, message):
    """
    If token given is authorised user, updates the message
    specified by message id with input message

    Arguments:
        token (str)          - unique str representation of user
        message_id (int))    - integer sppcifies message
        message (str)        - message that the user wishes to send

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - channel_id does not refer to valid channel
                    - length of message is over 1000 characters

    Return Value: N/A
    """
    store = data_store.get()

    # check message input is valid, otherwise raise input errors
    if not isinstance(message, str):
        raise InputError('Message is a string')

    if len(message) > 1000:
        raise InputError('Message must not exceed 1000 characters')

    # check valid token and user
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)
    check_valid_auth_id(auth_user_id)

    # check input message_id is valid and if exists
    message_data = check_message_id_valid(message_id)

    # check global owner case
    global_owner = check_user_is_global_owner(auth_user_id)
    channel = get_channel_id_with_message_id(message_id)
    
    # check is user is in the channel
    if check_user_is_member(auth_user_id, channel, 'all_members') is not None:
        if check_user_is_member(auth_user_id, channel, 'owner_members') is not None or \
            global_owner is True or message_data['u_id'] == auth_user_id:
            # if user is either owner or global owner or it's the user who sent the message
            message_data['message'] = message
            # delete message if input message is empty string
            if message == '':
                message_remove_v1(token, message_id)
        else:
            raise AccessError('User has no access to this specified message')
    else:
        raise AccessError('User has no access to this specified message')

    data_store.set(store)

    return {}

def message_remove_v1(token, message_id):
    """
    If token given is authorised user, remove the message
    specified by message id in channel/dm

    Arguments:
        token (str)          - unique str representation of user
        message_id (int))    - integer sppcifies message

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - channel_id does not refer to valid channel
                    - length of message is over 1000 characters

    Return Value: N/A
    """

    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)
    check_valid_auth_id(auth_user_id)
    # check input message_id is valid

    message_data = check_message_id_valid(message_id)

    # check global owner case
    global_owner = check_user_is_global_owner(auth_user_id)
    channel = get_channel_id_with_message_id(message_id)
    # is user is a global member and is member in the channel

    # check is user is in the channel
    if check_user_is_member(auth_user_id, channel, 'all_members') is not None:
        if check_user_is_member(auth_user_id, channel, 'owner_members') is not None or \
            global_owner is True or message_data['u_id'] == auth_user_id:
            # if user is either owner or global owner or it's the user who sent the message
            channel['messages'].remove(message_data)
        else:
            raise AccessError('User has no access to this specified message')
    else:
        raise AccessError('User has no access to this specified message')

    data_store.set(store)

    return {}

def message_senddm_v1(token, dm_id, message):
    """
    If token given is authorised user, sends the message
    to a specified dm with input dm_id

    Arguments:
        token (str)          - unique str representation of user
        dm_id (int))    - integer sppcifies dm
        message (str)        - message that the user wishes to send

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - dm_id does not refer to valid dm
                    - length of message is less than 1 or over 1000 characters

    Return Value:
        Message_id - int to specifies each message
    """

    message_id = send_message(token, dm_id, message, 'dm')

    return message_id

def get_channel_id_with_message_id(message_id):
    """
    finds and returns the channel data that the message_id is found in
    
    Arguments:
        message_id (int) - an integer that specifies a message

    Exceptions: N/A

    Return Value:
        Returns the channel data if the message_id is found
    """

    store = data_store.get()
    for channel in store['channels']:
        for message_data in channel['messages']:
            if message_data['message_id'] == message_id:
                return channel

def check_message_id_valid(message_id):
    """
    checks if the given message_id is valid by checking if it exists in stored
    data

    Arguments:
        message_id (int) - an int that specifies a message

    Exceptions:
        InputError - Raised if the message_id is of an invalid type, is less
                     than 1, or cannot be found in the stored data

    Return Value:
        Returns the channel's message data that the message_id is found in 
    """

    if isinstance(message_id, int) is False or type(message_id) == bool:
        raise InputError('Message id is not of a valid type')

    if message_id < 1:
        raise InputError('The message id is not valid (out of bounds)')

    # return message data if message id exists
    store = data_store.get()
    for channel in store['channels']:
        for message_data in channel['messages']:
            if message_data['message_id'] == message_id:
                return message_data

    # if message_id is not found, raise an InputError
    raise InputError('Message does not exist in channels database')

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
        raise AccessError(f'User does not exist in {data_str}')

    if not isinstance(message, str):
        raise InputError('Message is a string')

    if message == '':
        raise InputError('Empty message input')

    if len(message) > 1000:
        raise InputError('Message must not exceed 1000 characters')

    # increament message id for the store message
    message_id = new_id('message')

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
