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

from src.token import token_get_user_id, token_valid_check
from src.global_vars import new_message_id
from src.error import AccessError, InputError
import datetime

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

    for user in store['users']:
        if user['id'] == auth_user_id:
            user_info = user

    message_data = {
        'message_id': message_id, 
        'u_id': user_info['id'], 
        'message': message, 
        'time_sent': datetime.datetime.now()
    }


    channel_data['messages'].insert(0, message_data)

    data_store.set(store)

    return {
        'message_id': message_id
    }


# def message_edit_v1(token, channel_id, message):
# """
#     If token given is authorised user, updates the message
#     specified by message id with input message

#     Arguments:
#         token (str)          - unique str representation of user
#         message_id (int))    - integer sppcifies message
#         message (str)        - message that the user wishes to send

#     Exceptions:
#         AccessError - when message_id refers to a valid message in a joined channel/DM and none of the following are true:
#             - the message was sent by the authorised user making this request
#             - the authorised user has owner permissions in the channel/DM
#         InputError  - channel_id does not refer to valid channel
#                     - length of message is over 1000 characters

#     Return Value: N/A
#     """
#     store = data_store.get()

#     token_valid_check(token)
#     auth_user_id = token_get_user_id(token)
#     check_valid_auth_id(auth_user_id)
#     # check input message_id is valid
#     message_id = check_message_id_valid(message_id)

#     # check global owner case
#     has_perm = False
#     global_owner = check_user_is_global_owner(auth_user_id)
#     channel_id = get_channel_id_with_message_id(message_id)
#     # is user is a global member and is member in the channel
#     if check_user_is_member(auth_user_id, channel_id) != None and global_owner is True:
#         has_perm = True

#     user_is_owner = False
#     if check_user_is_owner_member(auth_user_id, channel_id) != None:
#         user_is_owner = True

#     for channel in store['channels']:
#         for message_data in channel['messages']:
#             if message_data['message_id'] == message_id:
#                 # check if message is sent by the user or user is owner
#                 if message_data['u_id'] == auth_user_id or has_perm is True or user_is_owner is True:
#                     channel['messages'].remove(message_data)
#                 else:
#                     raise AccessError('User has no access to this specified message')

#     data_store.set(store)

#     return {}

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
    channel_id = channel['channel_id']
    # is user is a global member and is member in the channel

    
    if check_user_is_member(auth_user_id, channel, 'all_members') is not None:
        print(f'user {auth_user_id} is in channel {channel_id}')
        if check_user_is_member(auth_user_id, channel, 'owner_members') is not None or global_owner is True or\
            message_data['u_id'] == auth_user_id:

            channel['messages'].remove(message_data)
        else:
            raise AccessError('User has no access to this specified message')
    else:
        raise AccessError('User has no access to this specified message')

    data_store.set(store)

    return {}

