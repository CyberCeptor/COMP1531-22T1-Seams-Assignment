"""
Filename: message.py

Author: Yangjun Yue(z5317840), Aleesha Bunrith(z5371516), Xingjian Dong(z5221888)
Created: 23/03/2022 - 14/04/2022

Description: implementation for
    - sending message to a specified channel or dm by an authorised user
    - given a specified message id and editing that message
    - removing specified message from a channel or dm
    - pinning a specified message from a channel or dm
    - reacting to a specified message from a channel or dm
    - helpers for the above
"""

from src.error import AccessError, InputError
from src.token import token_get_user_id, token_valid_check
from src.other import check_user_is_member, check_valid_dm_channel_id

from src.data_store import data_store

from src.global_vars import new_id

from src.message_helpers import check_message_id_valid, edit_react, \
                                edit_remove_dm_message_check, \
                                edit_remove_channel_message_check, \
                                pin_unpin_check_dm, pin_unpin_check_channel

from src.channel_dm_helpers import send_message, check_valid_message, \
                                   check_member_of_valid_dm_channel_id

@token_valid_check
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
    user_id = token_get_user_id(token)
    
    message_id = new_id('message')
    
    send_message(user_id, channel_id, '', message, message_id, 'channel', False, 
                False)

    return {
        'message_id': message_id
    }

@token_valid_check
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
    user_id = token_get_user_id(token)

    message_id = new_id('message')

    send_message(user_id, dm_id, '', message, message_id, 'dm', False, False)

    return {
        'message_id': message_id
    }

@token_valid_check
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

    check_valid_message(message)

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]
    
    if in_channel is False:
        edit_remove_dm_message_check(token, message, message_data, data, 'edit')
    else:
        edit_remove_channel_message_check(token, message, message_data, data, 
                                            'edit')

    data_store.set(store)

@token_valid_check
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

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]
    
    if in_channel is False:
        edit_remove_dm_message_check(token, '', message_data, data, 'remove')
    else:
        edit_remove_channel_message_check(token, '', message_data, data, 
                                            'remove')

    data_store.set(store)

@token_valid_check
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

    Return: N/A
    """

    auth_user_id = token_get_user_id(token)

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]

    if in_channel is False:
        pin_unpin_check_dm(auth_user_id, message_data, data, 'pin')
    else:
        pin_unpin_check_channel(auth_user_id, message_data, data, 'pin')

@token_valid_check
def message_unpin_v1(token, message_id):
    """
    If token given is authorised user, unpin the message
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
                    - message already unpinned

    Return: N/A
    """

    auth_user_id = token_get_user_id(token)

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]

    if in_channel is False:
        pin_unpin_check_dm(auth_user_id, message_data, data, 'unpin')
    else:
        pin_unpin_check_channel(auth_user_id, message_data, data, 'unpin')

@token_valid_check
def message_react_v1(token, message_id, react_id):
    """
    react to a specified message with a specific react

    Arguments:
        token (str)      - a user's valid jwt token
        message_id (int) - an int specifying a message sent in a channel or dm
        react_id (int)   - an int specifying a react

    Exceptions:
        AccessError - Raised if user has no access to the specified message
        InputError  - Raised if 
                        - message_id is not valid
                        - react_id is not valid
                        - message already contains the same react from the user

    Return Value: N/A
    """

    auth_user_id = token_get_user_id(token)

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]

    if in_channel is False:
        # if message was sent in a dm, check user is in dm
        if check_user_is_member(auth_user_id, data, 'members') is None:
            raise AccessError(description='User does not exist in dm')
    else:
        # if message was sent in a channel, check user is in channel
        if check_user_is_member(auth_user_id, data, 'all_members') is None:
            raise AccessError(description='User does not exist in channel')

    edit_react(auth_user_id, data, message_data, react_id, 'add')

@token_valid_check
def message_unreact_v1(token, message_id, react_id):
    """
    unreact to a specified message with a react id 1

    Arguments:
        token (str)      - a user's valid jwt token
        message_id (int) - an int specifying a message sent in a channel or dm
        react_id (int)   - an int specifying a react

    Exceptions:
        AccessError - Raised if user has no access to the specified message
        InputError  - Raised if 
                        - message_id is not valid
                        - react_id is not valid
                        - message has no react from the user

    Return Value: N/A
    """

    auth_user_id = token_get_user_id(token)

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]

    # if message is sent in dm
    if in_channel is False:
        # check if user is in dm
        if check_user_is_member(auth_user_id, data, 'members') is None:
            raise AccessError(description='User does not exist in dm')
    else:
        # if message was sent in a channel, check user is in channel
        if check_user_is_member(auth_user_id, data, 'all_members') is None:
            raise AccessError(description='User does not exist in channel')

    edit_react(auth_user_id, data, message_data, react_id, 'remove')

@token_valid_check
def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    """
    If token given is authorised user, share the message
    to a specified channel/dm with input channel_id/dm_id

    Arguments:
        token (str)          - unique str representation of user
        og_message_id (int)) - integer original message
        message (str)        - message that the user wishes to send
        channel_id (int))    - integer sppcifies channel
        dm_id (int))         - integer sppcifies dm

    Exceptions:
        AccessError - when og_message_id refers to a valid message in a joined 
            channel/DM and none of the following are true:
            - the message was sent by the authorised user making this request
            - the authorised user has owner permissions in the channel/DM
        InputError  - channel_id/dm_id does not refer to valid channel
                    - length of message is over 1000 characters

    Return Value:
        Shared_message_id - int to specifies shared message
    """
    
    auth_user_id = token_get_user_id(token)

    check_channel_dm_ids(channel_id, dm_id)

    if dm_id == -1:
        check_member_of_valid_dm_channel_id(auth_user_id, channel_id, 'channel')
    else: # channel_id == -1
        check_member_of_valid_dm_channel_id(auth_user_id, dm_id, 'dm')

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(og_message_id)
    og_message_data = check_return[0]

    og_message = og_message_data['message']

    shared_message_id = new_id('message')

    check_valid_message(message)

    # shared_message will look like:
    # <optional message>
    #     <message being shared>
    if message != '':
        shared_message = f'{message}\n\t{og_message}'
    else:
        shared_message = og_message

    if dm_id == -1:
        if message == '':
            # only send the original message to the channel
            send_message(auth_user_id, channel_id, message, og_message, 
                         shared_message_id, 'channel', False, True)
        else:
            # send the shared_message to the channel
            send_message(auth_user_id, channel_id, message, shared_message, 
                         shared_message_id, 'channel', False, True)

    if channel_id == -1:
        if message == '':
            # only send the original message to the channel
            send_message(auth_user_id, dm_id, message, og_message, 
                         shared_message_id, 'dm', False, True)
        else:
            # send the shared_message to the channel
            send_message(auth_user_id, dm_id, message, shared_message, 
                         shared_message_id, 'dm', False, True)

    return {
        'message_id': shared_message_id
    }

def check_channel_dm_ids(channel_id, dm_id):
    """
    checks if the given channel and dm ids from message/share are valid

    Arguments: 
        channel_id (int))    - integer sppcifies channel
        dm_id (int))         - integer sppcifies dm

    Exceptions: 
        InputError - Raised when 
                        - ids are of valid types
                        - when both are -1
                        - when one or the other isn't -1

    Return Value: N/A
    """

    check_valid_dm_channel_id(channel_id)
    check_valid_dm_channel_id(dm_id)

    if dm_id == -1 and channel_id == -1:
        raise InputError(description='Invalid ids')
    elif dm_id != -1 and channel_id != 1:
        raise InputError(description='Invalid ids')
