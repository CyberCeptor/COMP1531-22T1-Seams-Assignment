"""
Filename: channel_dm_helpers.py

Author: group
Created: 24/02/2022 - 27/03/2022

Description: helper functions used in channel and dm functions
    - getting messages from a channel or dm
    - sending a message to a channel or dm
    - checking if a dm id is valid
    - leaving a channel or dm
    - setting the is_this_user_reacted value
"""

import time

from src.error import InputError, AccessError
from src.other import check_user_is_member, check_valid_dm_channel_id, \
                      cast_to_int_get_requests, check_valid_dm_channel_id
from src.token import token_get_user_id, token_valid_check

from src.data_store import data_store

from src.notifications import tag_notification

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
    else: # data_str == 'dm'
        key = 'members'

    # check whether given user is in the given channel
    if check_user_is_member(auth_user_id, data, key) is None:
        raise AccessError(description=f'User does not exist in {data_str}')

    total_messages = len(data['messages'])

    start = check_start_valid(start, total_messages)

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
        to_return = add_messages_until_end(auth_user_id, data, start, 
                                           total_messages)
    else:
        set_is_this_user_reacted(auth_user_id, data['messages'], start, end)
        to_return = [data['messages'][index] for index in range(start, end)]

    return {
        'messages': to_return,
        'start': start,
        'end': end,
    }

def add_messages_until_end(auth_user_id, data, start, total_messages):
    """
    returns the message data in a channel or dm from index start to the end

    Arguments:
        auth_user_id (int)   - an integer that specifies a user
        data (dict)          - a dict storing the channel or dm info
        start (int)          - an int specifying the start index for the return 
                               of messages data
        total_messages (int) - number of total messages in the channel or dm

    Exceptions: N/A

    Return Value:
        Returns the list of message dicts
    """

    if start == total_messages - 1:
        # if there is only 1 message
        set_is_this_user_reacted(auth_user_id, data['messages'], start, 
                                    start + 1)
        to_return = [(data['messages'][start])]
    else:
        # if there are less than 50 messages from the index start or
        # if there are only 50 messages
        set_is_this_user_reacted(auth_user_id, data['messages'], start, 
                                    total_messages)
        to_return = [data['messages'][index] for index in
                        range(start, total_messages)]
    
    return to_return

def check_start_valid(start, total_messages):
    """
    checks if the given dm_id actually belongs to a dm

    Arguments: 
        start (int)          - an int specifying the start index for the return 
                               of messages data
        total_messages (int) - number of total messages in the channel or dm

    Exceptions: 
        InputError - Raised when start is
                        - not of a valid tpe
                        - a negative number
                        - larger than total_messages

    Return Value: 
        Returns start casted to an int if it is valid
    """

    # check start is of valid input type and input
    start = cast_to_int_get_requests(start, 'start')

    if start < 0:
        raise InputError(description='Invalid start')
    elif start > total_messages:
        raise InputError(description='Invalid start, not enough messages')
    
    return start

def send_message(auth_user_id, data_id, optional_msg, message, message_id, 
                option, standup, share):
    """
    Helper function for message/send and message/senddm: If token given is an
    authorised user, sends the message to a specified channel/dm with input
    data_id

    Arguments:
        auth_user_id (int) - unique int representation of user
        data_id (int)      - integer specifies a dm or channel
        optional_msg (str) - the optional message sent when sharing a message
        message (str)      - message that the user wishes to send
        message_id (int)   - generated id for the message
        option (str)       - a string used to print out any error messages if
                            InputError is raised and to check if message is 
                            being sent to a channel or dm
        standup (bool)     - denotes if the msg is being sent as a standup msg
        share (bool)       - denotes if the msg is being shared

    Exceptions:
        AccessError - Raised if the user is not a member of the channel or dm
        InputError  - Raised if message is not of a valid type or length

    Return Value:
        Message_id - int to specifies each message
    """

    store = data_store.get()

    data_info = check_member_of_valid_dm_channel_id(data_id)

    if message == '':
        raise InputError(description='Empty message input')

    check_valid_message(message)

    message_data = {
        'message_id': message_id, 
        'u_id': auth_user_id, 
        'message': message, 
        'time_sent': int(time.time()),
        'reacts': [{
            'react_id': 1,
            'u_ids': [],
            'is_this_user_reacted': False,
        }],
        'is_pinned': False
    }

    data_info['messages'].insert(0, message_data)

    data_store.set(store)

    # if the message is being sent as a standup message, do not send tag notifs
    # if the message is being shared, only send tag notifs from the optional_msg
    # otherwise, send tag notifs from the sent message
    if standup is False and share is False:
        tag_notification(auth_user_id, optional_msg, message, data_info, 
                         option)
    elif standup is False and share is True:
        tag_notification(auth_user_id, message, optional_msg, data_info, 
                         option)

def check_valid_message(message):
    """
    checks if the given message is valid

    Arguments: 
        message (str) - a message string that is being sent or edited

    Exceptions: 
        InputError - Raised when
                        - message is not a string
                        - message is too long

    Return Value: N/A
    """

    if not isinstance(message, str):
        raise InputError(description='Message is not a string')

    if len(message) > 1000:
        raise InputError(description='Message must not exceed 1000 characters')

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
def leave_channel_dm(token, auth_user_id, data_id, option):
    """
    Given a channel/dm id, remove the user given by token or auth_user_id from 
    that channel/dm

    Arguments: 
        token (str)        - a valid jwt token str
        auth_user_id (int) - an int representing a user
        data_id (int)      - the given channel or dm id
        option (str)       - a str denoting whether the user is leaving a dm
                             or channel

    Exceptions:
        Access Error - Raised when
                        - user is not a member of the channel or dm
                        - token is invalid
        Input Error - Raised when the given an invalid data_id

    Return Value: N/A
    """

    store = data_store.get()

    # if no auth_user_id is given, the user is trying to leave the channel/dm
    # themselves. otherwise, someone else is removing them
    if auth_user_id is None:
        auth_user_id = token_get_user_id(token)

    # if the user is being removed from/is leaving a dm
    if option == 'dm':
        dm = check_valid_dm_channel_id(data_id, 'dm', False)
        member_data = check_user_is_member(auth_user_id, dm, 'members')

        remove_from_dm(dm, member_data, auth_user_id)

    # if the user is being removed from/is leaving a channel
    if option == 'channel':
        channel = check_valid_dm_channel_id(data_id, 'channel', False)
        member_data = check_user_is_member(auth_user_id, channel, 'all_members')
        owner_data = check_user_is_member(auth_user_id, channel, 'owner_members')

        remove_from_channel(channel, member_data, owner_data)

    data_store.set(store)

def remove_from_dm(dm, member_data, auth_user_id):
    """
    Given the data of a dm, remove the user's member_data

    Arguments:
        dm (dict)          - the data corresponding to a specific dm
        member_data (dict) - the user's member_data stored in the dm
        auth_user_id (int) - an int representing a user

    Exceptions:
        Access Error - Raised when user is not a member of the dm

    Return Value: N/A
    """

    if member_data is None:
        raise AccessError(description='The user is not a member of dm')
    
    # if the user is the dm creator, make the creator data empty
    if dm['creator']['u_id'] == auth_user_id:
        dm['creator'] = {}
    dm['members'].remove(member_data)

def remove_from_channel(channel, member_data, owner_data):
    """
    Given the data of a channel, remove the user's member_data and/or owner_data

    Arguments:
        channel (dict)     - the data corresponding to a specific channel
        member_data (dict) - the user's member_data stored in the channel
        owner_data (dict)  - 

    Exceptions:
        Access Error - Raised when user is not a member of the channel

    Return Value: N/A
    """

    if member_data is None and owner_data is None:
        raise AccessError(description='User is not a member of channel')
    
    if owner_data is None:
        channel['all_members'].remove(member_data)
    else:
        # if the user is an owner_member, then they have to also be in
        # all_members user aswell.
        channel['all_members'].remove(member_data)
        channel['owner_members'].remove(owner_data)

def check_member_of_valid_dm_channel_id(auth_user_id, data_id, option):
    """
    checks if the given channel or dm id and if the user is a member

    Arguments: 
        auth_user_id (int) - an int representing a user
        data_id (int)      - integer specifies a dm or channel
        option (str)       - denotes whether it's a channel or dm

    Exceptions: 
        AccessError - Raised when user is not a member of the channel or dm

    Return Value:
        Returns the channel or dm data if the channel or dm is valid and the
        user is a member
    """

    # check if dm_id/channel_id are valid
    if option == 'channel':
        data_info = check_valid_dm_channel_id(data_id, 'channel', False)
        data_id = data_info['channel_id']
        key = 'all_members'
    else: # option == 'dm'
        data_info = check_valid_dm_channel_id(data_id, 'dm', False)
        data_id = data_info['dm_id']
        key = 'members'

    if check_user_is_member(auth_user_id, data_info, key) is None:
        raise AccessError(description=f'User is not a member of {option}')

    return data_info
