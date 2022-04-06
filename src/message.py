"""
Filename: message.py

Author: Yangjun Yue(z5317840)
Created: 23/03/2022 - 27/03/2022

Description: implementation for
    - sending message to a specified channel by an authorised user
    - given a specified message id and editing that message
    - removing specified message from channel
    - helpers for the above
"""

from src.admin import check_user_is_global_owner
from src.error import InputError, AccessError
from src.token import token_get_user_id, token_valid_check
from src.other import check_valid_auth_id, check_user_is_member, send_message

from src.data_store import data_store

def message_send_v1(token, channel_id, message):
    """
    If token given is authorised user, sends the message
    to a specified channel with input channel_id

    Arguments:
        token (str)          - unique str representation of user
        channel_id (int))    - integer sppcifies channel
        message (str)        - message that the user wishes to send

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined 
            channel/DM and none of the following are true:
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
        AccessError - when message_id refers to a valid message in a joined 
            channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - when message_id refers to an invalid message
                    - message is not a string
                    - length of message is over 1000 characters

    Return Value: N/A
    """

    store = data_store.get()

    # check message input is valid, otherwise raise input errors
    if not isinstance(message, str):
        raise InputError(description='Message is not a string')

    if len(message) > 1000:
        raise InputError(description='Message must not exceed 1000 characters')

    # check valid token and user
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)
    check_valid_auth_id(auth_user_id)

    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    channel_sent = check_return[1]
    info = check_return[2]
    
    if channel_sent is False:
        edit_remove_dm_message(token, message, message_data, info, 'edit')
    else:
        edit_remove_channel_message(token, message, message_data, info, 'edit')

    data_store.set(store)

def message_remove_v1(token, message_id):
    """
    If token given is authorised user, remove the message
    specified by message id in channel/dm

    Arguments:
        token (str)          - unique str representation of user
        message_id (int))    - integer sppcifies message

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined 
            channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - channel_id does not refer to valid channel
                    - length of message is over 1000 characters

    Return Value: N/A
    """

    store = data_store.get()
    # check valid token
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)
    check_valid_auth_id(auth_user_id)
    # check input message_id is valid

    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    channel_sent = check_return[1]
    info = check_return[2]
    
    if channel_sent is False:
        edit_remove_dm_message(token, '', message_data, info, 'remove')
    else:
        edit_remove_channel_message(token, '', message_data, info, 'remove')

    data_store.set(store)

def message_senddm_v1(token, dm_id, message):
    """
    If token given is authorised user, sends the message
    to a specified dm with input dm_id

    Arguments:
        token (str)          - unique str representation of user
        dm_id (int))    - integer sppcifies dm
        message (str)        - message that the user wishes to send

    Exceptions:
        AccessError - when message_id refers to a valid message in a joined 
            channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - dm_id does not refer to valid dm
                    - length of message is less than 1 or over 1000 characters

    Return Value:
        Message_id - int to specifies each message
    """

    message_id = send_message(token, dm_id, message, 'dm')

    return message_id

def check_message_id_valid(message_id):
    """
    checks if the given message_id is valid by checking if it exists in stored
    data

    Arguments:
        message_id (int) - an int that specifies a message

    Exceptions:
        InputError - Raised if the message_id is of an invalid type, has less
                     than 1 character, or cannot be found in the stored data

    Return Value:
        Returns
            - the message's associated data
            - the channel's or dm's message data that the message_id is found in
            - True if found in a channel, False if found in a dm
    """

    if isinstance(message_id, int) is False or type(message_id) == bool:
        raise InputError(description='Message id is not of a valid type')

    if message_id < 1:
        raise InputError(description='The message id is not valid \
            (out of bounds)')

    # return message data, True if found in channel, and channel/dm data 
    # if message id exists
    store = data_store.get()
    for channel in store['channels']:
        for message_data in channel['messages']:
            if message_data['message_id'] == message_id:
                return [message_data, True, channel]

    for dm in store['dms']:
        for message_data in dm['messages']:
            if message_data['message_id'] == message_id:
                return [message_data, False, dm]

    # if message_id is not found, raise an InputError
    raise InputError(description='Message does not exist in channels database')

def edit_remove_dm_message(token, message, msg_data, dm, option):
    """
    edits or removes a specified message sent in a dm

    Arguments:
        token (str)     - unique str representation of user
        message (str)   - message that the user wishes to send
        msg_data (dict) - the message's associated data
        dm (dict)       - the associate dm details that the message is found in
        option (str)    - specifies if the user is editing or removing the msg

    Exceptions:
        AccessError - If user has no access to the specified message

    Return Value: N/A
    """

    user_id = token_get_user_id(token)

    # if user is either creator or it's the user who sent the message
    if msg_data['u_id'] == user_id or dm['creator']['u_id'] == user_id:
        if option == 'remove':
            dm['messages'].remove(msg_data)
        elif option == 'edit' and message != '':
            msg_data['message'] = message
        elif option == 'edit' and message == '':
            # remove the message if the new message input is empty
            message_remove_v1(token, msg_data['message_id'])
    else:
        raise AccessError(description='User has no access to this message')

def edit_remove_channel_message(token, message, msg_data, channel, option):
    """
    edits or removes a specified message sent in a channel

    Arguments:
        token (str)     - unique str representation of user
        message (str)   - message that the user wishes to send
        msg_data (dict) - the message's associated data
        dm (dict)       - the associate dm details that the message is found in
        option (str)    - specifies if the user is editing or removing the msg

    Exceptions:
        AccessError - If user has no access to the specified message

    Return Value: N/A
    """

    user_id = token_get_user_id(token)

    # if user is either owner or it's the user who sent the message or
    # if user is a member in channel and is a global owner
    if (check_user_is_member(user_id, channel, 'owner_members') or
        msg_data['u_id'] == user_id or 
        (check_user_is_member(user_id, channel, 'all_members') and
        check_user_is_global_owner(user_id))):
        if option == 'remove':
            channel['messages'].remove(msg_data)
        elif option == 'edit' and message != '':
            msg_data['message'] = message
        elif option == 'edit' and message == '':
            # remove the message if the new message input is empty
            message_remove_v1(token, msg_data['message_id'])
    else:
        raise AccessError(description='User has no access to this message')



def message_pin_v1(token, message_id):
    """
    If token given is authorised user, pin the message
    specified by message id in channel/dm

    Arguments:
        token (str)          - unique str representation of user
        message_id (int))    - integer sppcifies message

    Exceptions:
        AccessError - message_id refers to a valid message in a joined 
        channel/DM and the authorised user does not have owner permissions
        in the channel/DM
        InputError  - message_id is not a valid message within a channel 
                    or DM that the authorised user has joined
                    - message already pinned

    Return Value: N/A
    """

    store = data_store.get()
    # check valid token
    token_valid_check(token)
    user_id = token_get_user_id(token)
    check_valid_auth_id(user_id)

    # check input message_id is valid
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    # specifies whether if it's channel or dm message
    channel_sent = check_return[1]
    # channel or dm info data
    info = check_return[2]
    
    # raise input error if message is already pinned
    key = 'is_pinned'
    if key in message_data:
        if message_data['is_pinned'] == True:
            raise InputError(description='Message is already pinned')

    # if message is sent in dm
    if channel_sent is False:
        # user is owner of dm
        if info['creator']['u_id'] == user_id:
            message_data['is_pinned'] = True
        else:
            raise AccessError(description='User has no access to this message')
    else:
        # if user is owner or global owner in channel
        if (check_user_is_member(user_id, info, 'owner_members') or 
        (check_user_is_member(user_id, info, 'all_members') and
        check_user_is_global_owner(user_id))):
            message_data['is_pinned'] = True
        else:
            raise AccessError(description='User has no access to this message')

    data_store.set(store)
