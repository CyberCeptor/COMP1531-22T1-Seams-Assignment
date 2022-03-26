"""
Filename: messages.py

Author: Yangjun Yue(z5317840)
Created: 23/03/2022

Description: implementation for
    - sending message to a specified channel by an authorised user
    - given a specified message id and editing that message
    - removing specified message from channel
"""

from src.data_store import data_store

from src.other import check_message_id_valid, check_valid_auth_id, check_valid_channel_id, \
    check_user_is_member, check_message_id_valid, get_channel_id_with_message_id
from src.admin import check_user_is_global_owner

from src.dm import check_valid_dm_id
from src.token import token_get_user_id, token_valid_check
from src.global_vars import new_message_id
from src.error import AccessError, InputError
import datetime
from datetime import timezone

from datetime import timezone

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

    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # see if given auth_user_id and channel_id are valid
    check_valid_auth_id(auth_user_id)
    channel_data = check_valid_channel_id(channel_id)
    channel_id = channel_data['channel_id']

    if check_user_is_member(auth_user_id, channel_data, 'all_members') is None:
        raise AccessError('User does not exist in channel')

    if not isinstance(message, str):
        raise InputError('Message is a string')

    if message == '':
        raise InputError('Empty message input')

    if len(message) > 1000:
        raise InputError('Message must not exceed 1000 characters')

    # increament message id for the store message
    message_id = new_message_id()

    time = datetime.datetime.now(timezone.utc)
    utc_time = time.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    message_data = {
        'message_id': message_id, 
        'u_id': auth_user_id, 
        'message': message, 
        'time_sent': utc_timestamp
    }

    channel_data['messages'].insert(0, message_data)

    data_store.set(store)

    return {
        'message_id': message_id
    }


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

    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # see if given auth_user_id and dm_id are valid
    check_valid_auth_id(auth_user_id)
    dm_info = check_valid_dm_id(dm_id)
    dm_id = dm_info['dm_id']

    if check_user_is_member(auth_user_id, dm_info, 'members') is None:
        raise AccessError('User does not exist in dm')

    if not isinstance(message, str):
        raise InputError('Message is a string')

    if message == '':
        raise InputError('Empty message input')

    if len(message) > 1000:
        raise InputError('Message must not exceed 1000 characters')

    # increament message id for the store message
    message_id = new_message_id()

    time = datetime.datetime.now(timezone.utc)
    utc_time = time.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    message_data = {
        'message_id': message_id, 
        'u_id': auth_user_id, 
        'message': message, 
        'time_sent': utc_timestamp
    }


    dm_info['messages'].insert(0, message_data)

    data_store.set(store)

    return {
        'message_id': message_id
    }