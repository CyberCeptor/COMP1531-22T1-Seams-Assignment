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

from src.other import check_valid_auth_id, check_valid_channel_id, check_user_is_member

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
        AccessError - channel_id is valid and the authorised user is not a member of the channel
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

    if check_user_is_member(auth_user_id, channel_id) is None:
        raise AccessError('User does not exist in channel')

    if not isinstance(message, str):
        raise InputError('Message is a string')

    if message == '':
        raise InputError('Empty message input')

    if len(message) > 1000:
        raise InputError('Message must not exceed 1000 characters')

    # increament message id for the store message
    message_id = new_message_id()
    print(message_id)

    for user in store['users']:
        if user['id'] == auth_user_id:
            user_info = user

    message_data = {
        'message_id': message_id, 
        'u_id': user_info['id'], 
        'message': message, 
        'time_sent': datetime.datetime.now()
    }

    store['channels']['messages'].insert(0, message_data)

    # for channel_info in store['channels']:
    #     channel_info['messages'].append(message_data)

    data_store.set(store)

    return {
        'channel_id': message_id
    }
