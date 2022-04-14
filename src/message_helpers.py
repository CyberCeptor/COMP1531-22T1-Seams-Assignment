"""
Filename: message.py

Author: Yangjun Yue(z5317840), Aleesha Bunrith(z5371516)
Created: 23/03/2022 - 07/04/2022

Description: herlper functions for
    - checking if a message id is valid
    - checking if a message can be edited or removed by the user
    - editing and removing a message
    - adding or removing a react to a message
"""

from src.error import InputError, AccessError
from src.other import check_user_is_member, check_user_is_global_owner
from src.token import token_get_user_id

from src.data_store import data_store

from src.notifications import tag_notification, react_notification

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
        edit_remove_message(user_id, dm, msg_data, message, option)
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
        edit_remove_message(user_id, channel, msg_data, message, option)
    elif (check_user_is_member(user_id, channel, 'all_members') and
        check_user_is_global_owner(user_id)):
        edit_remove_message(user_id, channel, msg_data, message, option)
    else:
        raise AccessError(description='User has no access to this message')

def edit_remove_message(auth_user_id, data, msg_data, message, option):
    """
    edits or removes a specified message

    Arguments:
        auth_user_id (int) - unique str representation of user
        message (str)      - message that the user wishes to send
        msg_data (dict)    - the message's associated data
        data (dict)        - the data of the channel or dm the message is in
        option (str)       - specifies if the user is editing or removing the msg
        option2 (str)      - specifies if the message is in a channel or dm

    Exceptions:
        AccessError - If user has no access to the specified message

    Return Value: N/A
    """

    if option == 'edit' and message != '':
        old_msg = msg_data['message']
        msg_data['message'] = message
        if 'channel_id' in data.keys():
            tag_notification(auth_user_id, old_msg, message, data, 'channel')
        else:
            tag_notification(auth_user_id, old_msg, message, data, 'dm')
    else: # if the new message input is empty or option == 'remove'
        data['messages'].remove(msg_data)

def edit_react(auth_user_id, data, message_data, react_id, option):
    """
    adds or removes the user's react to the reacts for the given message

    Arguments:
        auth_user_id (int)  - an int specifying a user
        data (dict)         - data for the channel or dm the message is in
        message_data (dict) - data for the message being reacted to
        react_id (int)      - an int specifying a react

    Exceptions:
        InputError  - Raised if 
                        - react_id is not valid
                        - message already contains the same react from the user

    Return Value: N/A
    """

    store = data_store.get()

    # check if react_id is valid, right now only react id 1 is valid
    if react_id != 1 or type(react_id) is bool:
        raise InputError(description='Invalid react id')

    if option == 'add':
        # check if user has already reacted to this message with react id 1
        if auth_user_id in message_data['reacts'][0]['u_ids']:
            raise InputError(description='User has already reacted with this react')

        # add the user id to the list of u_ids for react id 1
        message_data['reacts'][0]['u_ids'].append(auth_user_id)

        if 'channel_id' in data.keys():
            react_notification(auth_user_id, data, message_data, 'channel')
        else:
            react_notification(auth_user_id, data, message_data, 'dm')
    
    if option == 'remove':
        # check if user has reacted to this specific message
        if auth_user_id not in message_data['reacts'][0]['u_ids']:
            raise InputError(description='User has no react to this message')

        # add the user id to the list of u_ids for react id 1
        message_data['reacts'][0]['u_ids'].remove(auth_user_id)

    data_store.set(store)

def pin_unpin_check_dm(auth_user_id, message_data, data, option):
    """
    checks if a specified message sent in a dm can be pinned or unpinned by the 
    user

    Arguments:
        auth_user_id (int)  - an int specifying a user
        msg_data (dict)     - the message's associated data
        data (dict)         - data for the dm the message is in
        option (str)        - specifies if user is pinning or unpinning

    Exceptions:
        AccessError - If user is not an owner of the dm

    Return Value: N/A
    """

    # user must be owner of dm
    if data['creator']['u_id'] != auth_user_id:
        raise AccessError(description='User has no access to this message')
        
    pin_unpin(message_data, option)

def pin_unpin_check_channel(auth_user_id, message_data, data, option):
    """
    checks if a specified message sent in a channel can be pinned or unpinned by
    the user

    Arguments:
        auth_user_id (int)  - an int specifying a user
        msg_data (dict)     - the message's associated data
        data (dict)         - data for the channel the message is in
        option (str)        - specifies if user is pinning or unpinning

    Exceptions:
        AccessError - If user is in the channel but not a global owner

    Return Value: N/A
    """

    # user must be owner or global owner in channel
    if check_user_is_member(auth_user_id, data, 'owner_members') is None:
        raise AccessError(description='User has no access to this message')
    
    if not (check_user_is_member(auth_user_id, data, 'all_members') and
        check_user_is_global_owner(auth_user_id)):
        raise AccessError(description='User has no access to this message')
        
    pin_unpin(message_data, option)

def pin_unpin(message_data, option):
    """
    pins or unpins the given message

    Arguments:
        msg_data (dict) - the message's associated data
        option (str)    - specifies if user is pinning or unpinning

    Exceptions:
        InputError - Raised if message has already been pinned or unpinned

    Return Value: N/A
    """

    store = data_store.get()

    if option == 'pin':
        # raise input error if message is already pinned
        if message_data['is_pinned'] is True:
            raise InputError(description='Message is already pinned')

        print('is pinning message')
        message_data['is_pinned'] = True
    else: # option == 'unpin'
        # raise input error if message is already unpinned
        if message_data['is_pinned'] is False:
            raise InputError(description='Message is already unpinned')

        message_data['is_pinned'] = False

    data_store.set(store)
