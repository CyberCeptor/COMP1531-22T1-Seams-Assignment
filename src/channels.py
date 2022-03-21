"""
Filename: channels.py

Author: Jenson Morgan(z5360181), Yangjun Yue(z5317840)
Created: 24/02/2022 - 04/03/2022
from src.other import check_valid_auth_id
from src.other import check_user_is_member
Description: implementation for
    - creating either a public or a private channel with given name
    - listing all channels the user is part of and gives the channel id and name
    - listing all valid channels and provide their channel id and name
"""
from src.error import InputError
from src.other import check_valid_auth_id, check_user_is_member
from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id

def channels_list_v1(token):
    """
    Provides a channel list of all the public channels
    the user is a member of.

    Arguments:
        auth_user_id(int)    - must be a valid user id.

    Exceptions:
        null

    Return Value:
        Returns a dict containing the channel_id and name of the channels
        the user is a member of
    """

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    store = data_store.get()
    channels_list = []

    for channel in store['channels']:
        is_member = check_user_is_member(auth_user_id, channel['channel_id'])
        if is_member:
            channel_data = {
                'channel_id': channel['channel_id'],
                'name': channel['name'],
            }
            channels_list.append(channel_data)
    return {
        'channels': channels_list
    }


def channels_listall_v1(token):
    """
    check if user is valid then provides lists of diictionaries containing all
    channel ids and channel names

    Arguments:
        auth_user_id (int)      - an integer that specifies user id

    Exceptions:
        N/A

    Return Value:
        Returns list of dictionaries containing channel id as int
        and channel name as str
    """

    store = data_store.get()

    token_valid_check(token)

    # create list of dictionaries to store each channel_return
    dict_list = []
    for channel in store['channels']:
        channel_return = {
            'channel_id': channel['channel_id'],
            'name': channel['name']
        }
        dict_list.append(channel_return)

    # return lists of all channels(including private ones) with details
    return {
        'channels': dict_list
    }



# NNNEEEEEEEDDDDD TO CHANGE TO TOKEN< NOT AUTH_USED_ID
# LEAVING AS IS TO AVOID ERRORS IN OTHERS TESTS!!!!!

def channels_create_v1(token, name, is_public):
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

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    if len(name) > 20:
        raise InputError('The channel name must be less than 20 characters')

    if name == '':
        raise InputError('No channel name was entered')

    if not isinstance(is_public, bool):
        raise InputError('The public/private value given is not of type bool')

    # Loops through data_store['channels'] to check channel names if they
    # already exist. Having two channles with the same name is fine,
    # as long as they have different is_public values.
    for channel in store['channels']:
        if channel['name'] == name and channel['is_public'] == is_public:
            raise InputError('This channel name already exists')

    # get the number of channels created so far, incremented for the new channel
    # id.
    channel_id = len(store['channels']) + 1

    for user in store['users']:
        if user['id'] == auth_user_id:
            user_info = user

    # Storing the channel information
    channel_data = {
        'channel_id': channel_id,
        'name': name,
        'owner_members': [{
            'u_id': user_info['id'],
            'email': user_info['email'],
            'name_first': user_info['first'],
            'name_last': user_info['last'],
            'handle_str': user_info['handle']
        }],
        'all_members': [{
            'u_id': user_info['id'],
            'email': user_info['email'],
            'name_first': user_info['first'],
            'name_last': user_info['last'],
            'handle_str': user_info['handle']
        }],
        'is_public': is_public,
        'messages': []
    }

    store['channels'].append(channel_data)
    data_store.set(store)

    return {
        'channel_id': channel_id
    }
