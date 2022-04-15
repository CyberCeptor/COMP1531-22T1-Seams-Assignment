"""
Filename: notifications.py

Author: Aleesha Bunrith(z5371516)
Created: 10/04/2022

Description: implementation for
    - notifications/get/v1
    - helper functions for the above
        - checking if a user has been tagged in a message
        - adding a notification for a message react
        - adding a notification for being added to a channel
"""

from src.other import check_valid_auth_id, check_user_is_member
from src.token import token_valid_check, token_get_user_id

from src.data_store import data_store

@token_valid_check
def notifications_get_v1(token):
    """
    returns the 20 notifications the user received

    Arguments:
        token (str) - a valid jwt token str

    Exceptions: 
        AccessError - Raised if the token is invalid

    Return:
        Returns the list of notification dictionaries
    """

    auth_user_id = token_get_user_id(token)

    user = check_valid_auth_id(auth_user_id)

    user_notifs = user['all_data']['notifications']

    del user_notifs[20:]

    return {
        'notifications': user_notifs
    }

def tag_notification(auth_user_id, old_msg, new_msg, data, option):
    """
    creates a notification for any tagged user in a message that is being sent
    or edited

    Arguments:
        auth_user_id (int) - an int representing a user
        old_msg (str)      - the original message being edited, if a message is 
                             being sent then it will be an empty str
        new_msg (str)      - the message being sent or edited
        data (dict)        - the data of a channel or dm
        option (str)       - denotes whether the given data belongs to a channel 
                             or dm

    Exceptions: N/A

    Return: N/A
    """

    store = data_store.get()

    tagger = check_valid_auth_id(auth_user_id)['all_data']['handle']
    chan_dm_name = data['name']

    new_msg.lower()

    # find the indexes in the message where @'s are found
    find_ats = [idx for idx, char in enumerate(new_msg) if char == '@']

    handles = []

    # search if any handles can be found after each @
    for idx in find_ats:
        handles.append(get_handle(new_msg, idx))
    
    # iterate through all found handles, check if it belongs to a user, and 
    # check if the handle is included in the new_msg but not in the old_msg
    for return_data in handles:
        handle = return_data['handle']
        next_idx = return_data['end_idx']

        user = handle_get_user(handle[1:])

        # do not add the notification if the user is not in the channel or dm
        # or the handle does not belong to a user
        if user is None:
            pass
        elif not new_msg[next_idx].isalnum() or new_msg[next_idx].isspace():
            add_tag_notification(user, handle, new_msg, old_msg, data, option, tagger, chan_dm_name)
        
    data_store.set(store)

def add_tag_notification(user, handle, new_msg, old_msg, data, option, tagger, chan_dm_name):
    if handle in new_msg and handle not in old_msg.lower():
        # if the message being sent contains a tag then add a notification,
        # if the message is being edited and the original message does not
        # include the tag, add a notification,
        # if a message with a tag is being shared, only send a notification
        # if a user has been tagged in the optional message

        # notifications are ordered from most recent to least recent
        user['notifications'].insert(0, {
            'channel_id': data['channel_id'] if option == 'channel' else -1,
            'dm_id': data['dm_id'] if option == 'dm' else -1,
            'notification_message': 
                f'{tagger} tagged you in {chan_dm_name}: {new_msg[0:20]}'
        })

def get_handle(message, at_idx):
    """
    gets any possible handle str after the at_idx

    Exceptions: N/A

    Return:
        Returns all chars after the index of an @ until a non-alphanumeric char 
        is found
    """

    # https://stackoverflow.com/a/35231387


    idx = at_idx + 1

    while (idx < len(message) and 
        (message[idx].isalnum() or not message[idx].isspace())):
        idx += 1

    return {
        'handle': message[at_idx:idx],
        'end_idx': idx
    }

def handle_get_user(handle):
    """
    get the user data if the handle belongs to them

    Arguments:
        handle (str) - a handle str of a possible user

    Exceptions: N/A

    Return:
        Returns the user data if the handle belongs to them, otherwise return
        None if there is no user with that handle
    """

    store = data_store.get()

    for user in store['users']:
        if user['handle'] == handle:
            return user
    return None

def react_notification(auth_user_id, data, message_data, option):
    """
    creates a notification for the user whose messaged was reacted to

    Arguments:
        auth_user_id (int)  - an int representing a user
        data (dict)         - the data of a channel or dm
        message_data (dict) - data for the message being reacted to
        option (str)        - denotes whether the given data belongs to a 
                              channel or dm

    Exceptions: N/A

    Return: N/A
    """

    store = data_store.get()

    reactor = check_valid_auth_id(auth_user_id)['all_data']['handle']
    chan_dm_name = data['name']

    user_id = message_data['u_id']

    user = check_valid_auth_id(user_id)

    user_notifs = user['all_data']['notifications']

    if option == 'channel':
        key = 'all_members'
    else: # option == 'dm'
        key = 'members'

    # only add notification if user who originally sent the message is still
    # in the channel or dm
    if check_user_is_member(user['all_data']['id'], data, key):
        # notifications are ordered from most recent to least recent
        user_notifs.insert(0, {
            'channel_id': data['channel_id'] if option == 'channel' else -1,
            'dm_id': data['dm_id'] if option == 'dm' else -1,
            'notification_message': 
                f'{reactor} reacted to your message in {chan_dm_name}'
        })
    
    data_store.set(store)

def join_channel_dm_notification(auth_user_id, user_id, data, option):
    """
    creates a notification for a user who was added to a channel or dm

    Arguments:
        auth_user_id (int)  - an int representing a user who is adding another
                              to the channel or dm
        auth_user_id (int)  - an int representing the user being added to the 
                              channel or dm
        data (dict)         - the data of a channel or dm
        option (str)        - denotes whether the given data belongs to a 
                              channel or dm

    Exceptions: N/A

    Return: N/A
    """

    store = data_store.get()

    inviter = check_valid_auth_id(auth_user_id)['all_data']['handle']
    chan_dm_name = data['name']

    user = check_valid_auth_id(user_id)

    user_notifs = user['all_data']['notifications']

    # notifications are ordered from most recent to least recent
    user_notifs.insert(0, {
        'channel_id': data['channel_id'] if option == 'channel' else -1,
        'dm_id': data['dm_id'] if option == 'dm' else -1,
        'notification_message': f'{inviter} added you to {chan_dm_name}'
    })
    
    data_store.set(store)
    