"""
Filename: channels.py

Author: Jenson Morgan(),Yangjun Yue(5317840)
Created: 24/02/2022 - 04/03/2022

Description: implementation for
    - creating either a public or a private channel with given name
    - providing a list of channels the user is part of and give channel id and name
    - list all valid channels and provide their channel id and name
    - helper functions for the above
"""

from src.error import InputError
from src.other import check_valid_auth_id, check_user_is_member
from src.other import check_user_is_member
from src.data_store import data_store



def channels_list_v1(auth_user_id):

    if type(auth_user_id) != int:
        raise InputError("The ID must be of type int.")

    check_valid_auth_id(auth_user_id)

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






# Provide a list of all channels, including private channels, (and their associated details)

def channels_listall_v1(auth_user_id):
    """ check is user is valid then provides lists of diictionaries containing
    channel id and channel names

    Arguments:
        auth_user_id (int)      - an integer that specifies user id

    Exceptions:
        N/A

    Return Value:
        Returns list of dictionaries containing channel id as int
        and channel name as str
    """

    store = data_store.get()

    # check that the auth_user_id exists
    check_valid_auth_id(auth_user_id)

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
        "channels": dict_list
    }


    # Creates a new channel with the given name and is either public or private.
    # The user who created it automatically joins it.
    # Returns the channel id.

def channels_create_v1(auth_user_id, name, is_public):
    # retrieving channel data from data_store
    store = data_store.get()

    check_valid_auth_id(auth_user_id)

    if len(name) > 20:
        raise InputError("The channel name must be less than 20 characters.")

    if len(name) < 1:
        raise InputError("No channel name was entered.")

    if type(is_public) != bool:
        raise InputError("The public/private value given is not of type bool.")

    # Test channel names for repition, unless public vs private.
    # Loops through data_store['channels'] to check channel names if they already exist
    # and are of the same is_public (public/private) then cannot be created.
    # Having two channles with the same name is fine, as long as they have different is_public values.
    for channel in store['channels']:
        if channel['name'] == name and channel['is_public'] == is_public:
            raise InputError("This channel name already exists.")

    # get the number of channels created so far, incremented for the new channel id.
    channel_id = len(store['channels']) + 1

    # Storing the channel information 
    channel_data = {
        'channel_id': channel_id,
        'name': name,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'global_owners': [auth_user_id],
        'is_public': is_public,
    }

    store['channels'].append(channel_data)

    return {
        'channel_id': channel_id
    }
