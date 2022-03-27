"""
Filename: channel.py

Author: Jenson Morgan(z5360181), Yangjun Yue(z5317840), Zefan Cao(z5237177), Xingjian Dong (z5221888)
Created: 28/02/2022 - 06/03/2022

Description: implementation for
    - providing channel details including channel id and channel name with
        user id input
    - allowing members of both private and public channels to invite a valid
        user and add them to the channel
    - allowing authorised user to join a channel with channel id
    - return messages to channel authorised user
    - helper functions for the above
"""

from src.error import InputError, AccessError
from src.other import check_valid_auth_id, get_messages
from src.other import check_user_is_member, check_valid_channel_id, check_user_is_global_owner
from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id

def channel_invite_v2(token, channel_id, u_id):
    """
    check if given user id and channel id are valid,
    and then add the user into the channel with u_id, channel_id, token
    return nothing

    Arguments:
        token (str)    - unique str representation of user
        channel_id (int) - an integer that specifies channel id
        u_id (int) - an integer that specifies user(invitee) id

    Exceptions:
        InputError - Occurs if the user id(invitee) is already exist in channel
        AccessError - Occurs if the user id(inviter) is not in channel

    Return Value: N/A
    """
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    check_valid_auth_id(auth_user_id) # check the inviter is valid or not
    check_valid_auth_id(u_id)# check the invitee is valid or not
    # check the channel is valid or not
    channel_data = check_valid_channel_id(channel_id)
    # if auth_user_id is a member of the channel and u_id isn't
    # then add u_id into the channel
    if check_user_is_member(auth_user_id, channel_data, 'all_members') is None:
        raise AccessError(description='Inviter is not in the channel')
    
    if check_user_is_member(u_id, channel_data, 'all_members') is not None:
        raise InputError(description='Invitee is already in the channel')
    else:
        add_invitee(u_id, channel_data) #add user
    return {
    }

def channel_details_v2(token, channel_id):
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

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # see if given auth_user_id and channel_id are valid
    check_valid_auth_id(auth_user_id)
    channel_info = check_valid_channel_id(channel_id)

    # is_member is a bool to check whether given user is in the given channel
    if check_user_is_member(auth_user_id, channel_info, 'all_members') is None:
        raise AccessError(description='User does not exist in channel')

    #return requires keys and values from stored data
    return {
        'name': channel_info['name'],
        'is_public': channel_info['is_public'],
        'owner_members': channel_info['owner_members'],
        'all_members': channel_info['all_members'],
    }

def channel_messages_v2(token, channel_id, start):
    """
    check if given user id and channel id are valid,
    check start not overflow in channel,
    return messages to a channel authorised user,
    if too much messages do pagination operate.

    Arguments:
        auth_user_id (int)    - an integer that specifies user id
        channel_id (int) - an integer that specifies channel id
        start (int) - an integer that specifies index for message

    Exceptions:
        AccessError - Occurs if the user id does not exist in channel

    Return Value:
        Returns a dictionary containing message_id, u_id, message, time_sent,
        start and end if given user id and channel id are valid
    """
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # see if given auth_user_id and channel_id are valid
    check_valid_auth_id(auth_user_id)
    channel_data = check_valid_channel_id(channel_id)

    messages = get_messages(auth_user_id, channel_data, start, "channel")

    return messages

def channel_join_v2(token, channel_id):
    """
    check if given user id and channel id are valid,
    and then add the user into the channel with channel_id
    return nothing

    Arguments:
        token (string)    - unique str representation of user
        channel_id (int) - an integer that specifies channel id

    Exceptions:
        InputError - Occurs if the user id(invitee) is already exist in channel

    Return Value: N/A
    """
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    check_valid_auth_id(auth_user_id)   #check the invitee is valid or not
    # check the channle is valid or not
    channel_data = check_valid_channel_id(channel_id)

    #check the invitee whether is already in the channel
    if check_user_is_member(auth_user_id, channel_data, 'all_members') is not None:
        raise InputError(description='Invitee is already in the channel')

    # check if the user is a global owner
    # if not, check if it is a private channel
    if check_user_is_global_owner(auth_user_id) is False:
        if channel_data['is_public'] is False:
            raise AccessError('Channel is private')
    
    # if the user is a global owner and the channel is private, or if the user
    # is not a global owner and the channel is public, add them to the channel
    add_invitee(auth_user_id, channel_data) #add user

def add_invitee(u_id, channel):
    """
    add the user into the channel with channel_id

    Arguments:
        u_id (int)    - an integer that specifies user(invitee) id
        channel_id (int) - an integer that specifies channel id

    Exceptions: N/A

    Return Value: N/A
    """
    store = data_store.get()

    for user in store['users']:
        if user['id'] == u_id:
            user_info = user

    new_member = {
        'u_id': user_info['id'],
        'email': user_info['email'],
        'name_first': user_info['first'],
        'name_last': user_info['last'],
        'handle_str': user_info['handle']
    }

    channel['all_members'].append(new_member)
    data_store.set(store)

def channel_leave_v1(auth_user_id, channel_id):
    """
    Given a channel_id that the authorised user is a member of, remove them as a member 
    of the channel. Their messages should remain in the channel. If the only channel owner leaves, 
    the channel will remain.
    If a user is a owner_members of a channel, they have to be an all_members user aswell.

    Arguments:
        -   token (string)
        -   channel_id  (int)

    Exceptions:
        AccessError - Occurs when the user_id returned from the token is not a member of
                        that channel, i.e. not in all_members.

    Return Value: 
                N/A
    """
    store = data_store.get()
    channel_data = check_valid_channel_id(channel_id)
    member_data = check_user_is_member(auth_user_id, channel_data, 
                                       'all_members')
    owner_data = check_user_is_member(auth_user_id, channel_data, 
                                      'owner_members')

    # if the user is an owner_member, then they have to also be an
    # all_members user aswell.
    if owner_data:
        channel_data['all_members'].remove(member_data)
        channel_data['owner_members'].remove(owner_data)
    elif member_data:
        channel_data['all_members'].remove(member_data)
    else:
        raise AccessError(description='User is not a member of that channel')

    data_store.set(store)
    return {}




# If the user is a member of the channel, and a global owner of SEAMS,
# they can add remove whoever they like, including themselves.
def channel_addowner_v1(token, channel_id, u_id):
    """
    Make user with user id u_id an owner of the channel.
    POST
    Arguments:
            - token (of owner_member adding the other user)
            - channel_id (the channel to add the owner too)
            - u_id (the user_id of the member being added to owners)

    Exceptions:
        InputError:
            - channel_id does not refer to valid channel
            - u_id does not refer to a valid user
            - u_id refers to a user who is not a member of the channel
            - u_id refers to a user who is already an owner of the channel

        AccessError:
            - channel_id is valid and the authorised user does not have permissions in the channel
    Return Value:
            N/A - Returns an empty dict.
    """
    channel_addremove_owner_valid_check(token, channel_id, u_id, 'add')
    return {}




def channel_removeowner_v1(token, channel_id, u_id):
    """
    Remove user with user id u_id as an owner of the channel
    POST
    Arguments:
            - token (the token of an authorised owner_members)
            - channel_id (channel to remove the user_id from)
            - u_id (id of member to remove from owner_members)

    Exceptions:
        InputError:
            - channel_id does not refer to valid channel
            - u_id does not refer to a valid user
            - u_id refers to a user who is not an owner of the channel
            - u_id refers to a user who is currently the only owner of the channel
        AccessError:
            - channel_id is valid and the authorised user does not have owner permissions in the channel

    Return Value:
                N/A
    """
    channel_addremove_owner_valid_check(token, channel_id, u_id, 'remove')
    return {}

'''As both add/reove owner share the same code, apart from the last statement,
this function performs both, but containts a 4th argument to differentiate between them.'''
def channel_addremove_owner_valid_check(token, channel_id, u_id, option):
    store = data_store.get()
    token_valid_check(token)
    check_valid_auth_id(u_id)
    channel_data = check_valid_channel_id(channel_id)
    inviter_user_id = token_get_user_id(token)

    # if check_user_is_member returns None, they are not a member of the channel, raise error
    # if they are, check if there perm_id == 1, if it is, they have permission to add user.
    setter_channel_data = check_user_is_member(inviter_user_id, channel_data, 'all_members')
    if setter_channel_data == None:
        raise AccessError(description='Not a member of the channel')

    member_data = check_user_is_member(u_id, channel_data, 'all_members')
    if member_data is None:
        raise InputError(description='User is not a valid member.')

    if check_user_is_global_owner(inviter_user_id):
        pass
    elif check_user_is_member(inviter_user_id, channel_data, 'owner_members') is None:
        raise AccessError(description='The inviter is not an owner_member')

    if option == 'add':
        # check that the user_id isn't already a owner_member
        if check_user_is_member(u_id, channel_data, 'owner_members'):
            raise InputError(description='The user is already an owner_member')
        #add the member_data to the owner_members_dict
        channel_data['owner_members'].append(member_data)
    elif option == 'remove':
        if check_user_is_member(u_id, channel_data, 'owner_members') is None:
            raise InputError(description='The user is already an owner_member')
        # Need to check the number of members in owner_members,
        # if the member being removed is the only member, raise InputError.
        if len(channel_data['owner_members']) == 1:
            raise InputError(description='This is the only owner_member left in the channel')
        channel_data['owner_members'].remove(member_data)

    data_store.set(store)