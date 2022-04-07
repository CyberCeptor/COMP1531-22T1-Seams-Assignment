"""
Filename: message.py

Author: Yangjun Yue(z5317840), Aleesha Bunrith(z5371516)
Created: 23/03/2022 - 07/04/2022

Description: implementation for
    - sending message to a specified channel or dm by an authorised user
    - given a specified message id and editing that message
    - removing specified message from a channel or dm
    - pinning a specified message from a channel or dm
    - reacting to a specified message from a channel or dm
    - helpers for the above
"""

from src.error import InputError, AccessError
from src.token import token_get_user_id, token_valid_check
from src.other import check_user_is_member, check_user_is_global_owner, \
                      send_message, check_valid_auth_id

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

def edit_remove_dm_message_check(token, message, msg_data, dm, option):
    """
    checks if a specified message sent in a dm can be edited or removed by the 
    user

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
        edit_remove_message(dm, msg_data, message, option)
    else:
        raise AccessError(description='User has no access to this message')

def edit_remove_channel_message_check(token, message, msg_data, channel, option):
    """
    checks if a specified message sent in a channel can be edited or removed by 
    the user

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
        msg_data['u_id'] == user_id):
        edit_remove_message(channel, msg_data, message, option)
    elif (check_user_is_member(user_id, channel, 'all_members') and
        check_user_is_global_owner(user_id)):
        edit_remove_message(channel, msg_data, message, option)
    else:
        raise AccessError(description='User has no access to this message')

def edit_remove_message(data, msg_data, message, option):
    """
    edits or removes a specified message

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

    if option == 'remove':
        data['messages'].remove(msg_data)
    elif option == 'edit' and message != '':
        msg_data['message'] = message
    elif option == 'edit' and message == '':
        # remove the message if the new message input is empty
        data['messages'].remove(msg_data)

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

    store = data_store.get()
    # check valid token
    token_valid_check(token)
    user_id = token_get_user_id(token)

    # check input message_id is valid and return the message_data, if the 
    # message was sent in a channel or dm, and the corresponding channel or dm 
    # data
    check_return = check_message_id_valid(message_id)
    message_data = check_return[0]
    in_channel = check_return[1]
    data = check_return[2]
    
    # raise input error if message is already pinned
    if message_data['is_pinned'] is True:
        raise InputError(description='Message is already pinned')

    # if message is sent in dm
    if in_channel is False:
        # user is owner of dm
        if data['creator']['u_id'] == user_id:
            message_data['is_pinned'] = True
        else:
            raise AccessError(description='User has no access to this message')
    else:
        # if user is owner or global owner in channel
        if (check_user_is_member(user_id, data, 'owner_members') or 
        (check_user_is_member(user_id, data, 'all_members') and
        check_user_is_global_owner(user_id))):
            message_data['is_pinned'] = True
        else:
            raise AccessError(description='User has no access to this message')

    data_store.set(store)

def search_v1(token, query_str):
    """
    If token given is authorised user, return a collection of messages
    in all of the channels/DMs that the user has joined that contain 
    the query (case-insensitive). There is no expected order for these messages.

    Arguments:
        token (str)          - unique str representation of user
       query_str (str)       - str that searches for matching messages

    Exceptions:
        InputError  - length of query_str is less than 1 or over 1000 characters
    """
    
    # getting information from date_store
    store = data_store.get()
    # check valid token
    token_valid_check(token)
    user_id = token_get_user_id(token)
    check_valid_auth_id(user_id)

    # checking query string input
    if query_str == '':
        raise InputError(description='Empty query string input')

    if len(query_str) > 1000:
        raise InputError(description='Message must not exceed 1000 characters')

    
    # create a list to store all correlated messages and return in the end
    message_return = []
    for channel in store['channels']:
        for message_data in channel['messages']:
            # account case insensitivity
            if (query_str.lower() in message_data['message'].lower() and 
            check_user_is_member(user_id, channel, 'all_members') is not None):
                    message_return.append(message_data)

    # checking dm case                
    for dm in store['dms']:
        for message_data in dm['messages']:
            # account case insensitivity
            if (query_str.lower() in message_data['message'].lower() and 
            check_user_is_member(user_id, dm, 'members') is not None):
                    message_return.append(message_data)

    return message_return

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

    store = data_store.get()

    # check valid token
    token_valid_check(token)
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

    # check if react_id is valid, right now only react id 1 is valid
    if react_id != 1 or type(react_id) is bool:
        raise InputError(description='Invalid react id')

    # check if user has already reacted to this message with react id 1
    if auth_user_id in message_data['reacts'][0]['u_ids']:
        raise InputError(description='User has already reacted with this react')

    # add the user id to the list of u_ids for react id 1
    message_data['reacts'][0]['u_ids'].append(auth_user_id)

    data_store.set(store)
