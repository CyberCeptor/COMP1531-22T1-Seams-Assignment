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

from src.other import check_valid_auth_id
from src.token import token_valid_check, token_get_user_id

from src.data_store import data_store

def check_for_tags(auth_user_id, old_msg, new_msg, data, option):
    """
    checks if there are any tags in the message and creates a notification for 
    the tagged user if any are found

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

    # iterate through all user handles and check if the handle is included in 
    # the message after an @
    for user in store['users']:
        handle = user['handle']

        # if the message being sent contains a tag then add a notification
        # if the message is being edited and the original message does not
        # include the tag, add a notification
        if f'@{handle}' in new_msg.lower() and f'@{handle}' not in old_msg.lower():
            # notifications are ordered from most recent to least recent
            user['notifications'].insert(0, {
                'channel_id': data['channel_id'] if option == 'channel' else -1,
                'dm_id': data['dm_id'] if option == 'dm' else -1,
                'notification_message': 
                    f'{tagger} tagged you in {chan_dm_name}: {new_msg[0:20]}'
            })
    
    data_store.set(store)

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
