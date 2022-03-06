"""
Filename: channel.py

Author: Yangjun Yue(z5317840), Zefan Cao(z5237177)
Created: 28/02/2022 - 04/03/2022

Description: implementation for
    - providing channel details including channel id and channel name with
        user id input
    - allowing members of both private and public channels to invite a valid
        user and add them to the channel
    - allowing authorised user to join a channel with channel id
    - helper functions for the above
"""

from src.error import InputError, AccessError
from src.other import check_valid_auth_id
from src.other import check_user_is_member, check_valid_channel_id

from src.data_store import data_store

def channel_invite_v1(auth_user_id, channel_id, u_id):
    """
    check if given user id and channel id are valid,
    and then add the user into the channel with u_id, channel_id
    return nothing

    Arguments:
        auth_user_id (int)    - an integer that specifies user(inviter) id
        channel_id (int) - an integer that specifies channel id
        u_id (int) - an integer that specifies user(invitee) id

    Exceptions:
        InputError - Occurs if the user id(invitee) is already exist in channel
        AccessError - Occurs if the user id(inviter) is not in channel

    Return Value: N/A
    """
    check_valid_auth_id(auth_user_id) # check the inviter is valid or not
    check_valid_auth_id(u_id)# check the invitee is valid or not
    check_valid_channel_id(channel_id) # check the channel is valid or not
    # if auth_user_id is a member of the channel and u_id isn't
    # then add u_id into the channel
    if check_user_is_member(auth_user_id, channel_id) is False:
        raise AccessError('Inviter is not in the channel')
    if check_user_is_member(auth_user_id, channel_id) is True:
        if check_user_is_member(u_id, channel_id) is True:
            raise InputError('Invitee is already in the channel')
    else:
        add_invitee(u_id, channel_id) #add user
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    """
    check if given user id and channel id are valid,
    return details about the channel including channel name, publicity, owner
    members and all members with given user id and channel id.

    Arguments:
        auth_user_id (int)    - an integer that specifies user id
        channel_id (int) - an integer that specifies channel id

    Exceptions:
        InputError - Occurs if the user id does not exist in channel

    Return Value:
        Returns a dictionary containing channel name, publicity of the channel,
        owner members and all members if given user id and channel id are valid
    """

    store = data_store.get()

    # see if given auth_user_id and channel_id are valid
    check_valid_auth_id(auth_user_id)
    check_valid_channel_id(channel_id)

    # is_member is a bool to check whether given user is in the given channel
    is_member = check_user_is_member(auth_user_id, channel_id)
    if is_member is False:
        raise InputError('User does not exist in channel')

    # channel id starts at 1, so -1 to get the correct dict
    channel = store['channels'][channel_id - 1]

    #return requires keys and values from stored data
    return {
        'name': channel['name'],
        'is_public': channel['is_public'],
        'owner_members': channel['owner_members'],
        'all_members': channel['all_members'],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_sent': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    """
    check if given user id and channel id are valid,
    and then add the user into the channel with channel_id
    return nothing

    Arguments:
        auth_user_id (int)    - an integer that specifies user(inviter) id
        channel_id (int) - an integer that specifies channel id

    Exceptions:
        InputError - Occurs if the user id(invitee) is already exist in channel

    Return Value: N/A
    """
    check_valid_auth_id(auth_user_id)   #check the invitee is valid or not
    check_valid_channel_id(channel_id)  #check the channle is valid or not

    #check the invitee whether is already in the channel
    if check_user_is_member(auth_user_id, channel_id) is True:
        raise InputError('Invitee is already in the channel')

    #check the user whether is a global owner
    #if the user is a global owner, add immediately, even this is a priavate
    # channel
    if check_user_is_global_owner(auth_user_id, channel_id) is True:
        add_invitee(auth_user_id, channel_id) # add user

    check_public_channel(channel_id) #check the channel whether is public
    add_invitee(auth_user_id, channel_id) #add user

def add_invitee(u_id, channel_id):
    """
    add the user into the channel with channel_id

    Arguments:
        u_id (int)    - an integer that specifies user(invitee) id
        channel_id (int) - an integer that specifies channel id

    Exceptions: N/A

    Return Value: N/A
    """
    store = data_store.get()

    channel = store['channels'][channel_id - 1]
    channel['all_members'].append(u_id)
    data_store.set(store)

def check_user_is_global_owner(auth_user_id, channel_id):
    """
    check the user whether is a global owner in channel
    with auth user id and channel id, return nothing

    Arguments:
        auth_user_id (int)    - an integer that specifies user(inviter) id
        channel_id (int) - an integer that specifies channel id

    Exceptions: N/A

    Return Value: N/A
    """
    store = data_store.get()

    channel = store['channels'][channel_id - 1]
    if auth_user_id in channel['global_owners']:
        return True
    return False

def check_public_channel(channel_id):
    """
    check the channel is public or not with channel id
    return nothing

    Arguments:
        channel_id (int) - an integer that specifies channel id

    Exceptions:
        AccessError - Occurs if the channel(channel id == False) is private

    Return Value: N/A
    """
    store = data_store.get()

    channel = store['channels'][channel_id - 1]
    if channel['is_public'] is False:
        raise AccessError('Channel is private')
