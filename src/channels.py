"""
Filename: channels.py

Author: Jenson Morgan(z5360181), Yangjun Yue(z5317840)
Created: 24/02/2022 - 04/03/2022

Description: implementation for
    - creating either a public or a private channel with given name
    - listing all channels the user is part of and gives the channel id and name
    - listing all valid channels and provide their channel id and name
"""

from src.error import InputError
from src.other import check_valid_auth_id, check_user_is_member
from src.token import token_valid_check, token_get_user_id

from src.data_store import data_store

@token_valid_check
def channels_list_v2(token):
    """
    Validates the user token, gets the user_id from the decoded
    token, validates the user id, searches all channels and 
    appends the channel name and id when the user is a member.

    Channels_list will be ordered by the channel_id, so regardless
    of when the user joins the channel, the return value will be ordered
    by the lowest value channel_id first to the next greatest value.

    Arguments:
        token   - token must be valid.

    Exceptions: N/A

    Return Value:
        Returns a dict containing the channel_id and name of the channels
        the user is a member of
    """

    auth_user_id = token_get_user_id(token)

    check_valid_auth_id(auth_user_id)

    store = data_store.get()
    channels_list = []

    for channel in store['channels']:
        if check_user_is_member(auth_user_id, channel, 'all_members'):
            channel_data = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
            channels_list.append(channel_data)

    return {
        'channels': channels_list
    }

@token_valid_check
def channels_listall_v2(token):
    """
    check if user is valid then provides lists of diictionaries containing all
    channel ids and channel names

    Arguments:
        auth_user_id (int)      - an integer that specifies user id

    Exceptions: N/A

    Return Value:
        Returns list of dictionaries containing channel id as int
        and channel name as str
    """

    store = data_store.get()

    auth_user_id = token_get_user_id(token)

    # check that the auth_user_id exists
    check_valid_auth_id(auth_user_id)

    # return lists of all channels(including private ones) with details
    return {
        'channels': [{
            'channel_id': channel['channel_id'],
            'name': channel['name']
        } for channel in store['channels']]
    }

@token_valid_check
def channels_create_v2(token, name, is_public):
    """
    Creates a new channel with the name and is_public status given.
    The creating member is an owner_member and has permissions to
    add and remove other members.

    Arguments:
        auth_user_id (int)  - a valid int user_id
        name (str)          - a string that is unique
            (i.e. a channel can have the same name, as long as they differ
                in public/private)
        is_public (boolean) - a bool to state its public/private value
                                (True == public)

    Exceptions:
        AccessError - Occurs when the given user_id does not exist in Seams
        InputError  - Occurs when the channel name given is less than 1
                        character and greater than 20 characters
                    - Occurs when is_public is not a bool
                    - Occurs when the channel name and is_public combo already
                        exists

    Return Value:
        Returns a dict containing the channel_id, name, owner_members,
            all_members, global_owners, is_public
    """

    store = data_store.get()

    auth_user_id = token_get_user_id(token)

    user_info = check_valid_auth_id(auth_user_id)

    if len(name) > 20:
        raise InputError(description='The channel name must be less than 20 \
                                      characters')

    if name == '':
        raise InputError(description='No channel name was entered')

    if not isinstance(is_public, bool):
        raise InputError(description='The public/private value given is not of\
                                      type bool')

    # Loops through data_store['channels'] to check channel names if they
    # already exist. Having two channles with the same name is fine,
    # as long as they have different is_public values.
    for channel in store['channels']:
        if channel['name'] == name and channel['is_public'] == is_public:
            raise InputError(description='This channel name already exists')

    # get the number of channels created so far, incremented for the new channel
    # id.
    channel_id = len(store['channels']) + 1

    # Storing the channel information
    channel_data = {
        'channel_id': channel_id,
        'name': name,
        'owner_members': [user_info['return_data']],
        'all_members': [user_info['return_data']],
        'is_public': is_public,
        'messages': [], 
        'standup': {
            'is_active': False,
            'time_finish': None,
        }
    }

    store['channels'].append(channel_data)
    data_store.set(store)

    return {
        'channel_id': channel_id
    }
