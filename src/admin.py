"""
Filename: admin.py

Author: Aleesha, z5371516
Created: 22/03/22 - 27/03/2022

Description: implementation for
    - changing the permission of a specified user
    - removing a user from Seams
    - helper functions for the above
"""

from src.dm import dm_leave_v1

from src.error import AccessError, InputError
from src.other import check_valid_auth_id, check_user_is_global_owner,\
                      check_user_is_member
from src.token import token_valid_check, token_get_user_id

from src.channel import channel_leave_v1

from src.data_store import data_store

def admin_userpermission_change(token, u_id, permission_id):
    """
    changes the permission of a specified user using a global owner's token

    Arguments:
        token (jwt token str) - a user's valid jwt token
        u_id (int)            - an int representing a user
        permission_id (int)   - an int representing a user permission

    Exceptions:
        InputError  - Raised when 
                        - the token belongs to a user who is not a global owner
                        - the permission id is of a invalid type
                        - the permission id is an invalid integer
                        - there is only one global owner and they are trying to
                          demote themselves to a normal user
                        - the user is already a global owner
                        - the user is already a normal user
        AccessError - Raised when someone who is not a global owner is trying to
                      change another user's permissions

    Return Value: N/A
    """

    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # the token must belong to a user who is a global owner
    if not check_user_is_global_owner(auth_user_id):
        raise AccessError(description='User is not a global owner')

    check_valid_auth_id(u_id)

    # check for invalid permission_id inputs
    if not isinstance(permission_id, int) or type(permission_id) is bool:
        raise InputError(description='Permission id is not of valid type')

    if permission_id not in [1, 2]:
        raise InputError(description='Invalid permission id')

    # count the number of global users
    num_global_owners = len([user for user in store['users'] if 
                             user['perm_id'] == 1])

    # check three invalid cases of permission changes
    if (check_user_is_global_owner(u_id) and num_global_owners == 1 and
        permission_id == 2):
        raise InputError(description='Cannot demote the only global owner')
    elif check_user_is_global_owner(u_id) and permission_id == 1:
        raise InputError(description='User is already a global owner')
    elif not check_user_is_global_owner(u_id) and permission_id == 2:
        raise InputError(description='User is already a member')

    change_permission(u_id, permission_id)

def admin_user_remove(token, u_id):
    """
    removes a user from Seams, they will be removed from all channels and dms,
    their messages will be replaced by 'Removed user' and their email and handle
    can be reused

    Arguments:
        token (jwt token str) - a valid jwt token
        u_id (int)            - an int representing a user

    Exceptions:
        InputError  - Raised when the only global owner is trying to remove
                      themselves
        AccessError - Raised when someone who is not a global owner is trying to
                      remove a user

    Return Value: N/A
    """

    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)
    user_data = check_valid_auth_id(u_id)
 
    # if user with the token is not a global owner, they cannot remove a user
    if check_user_is_global_owner(auth_user_id) is False:
        raise AccessError(description='User is not a global owner')

    # if there is only one global owner, they cannot remove themselves
    num_global_owners = len([user for user in store['users'] if 
                             user['perm_id'] == 1])

    if check_user_is_global_owner(u_id) and num_global_owners == 1:
        raise InputError(description='Cannot remove the only global owner')

    # remove user from all channels, replace their messages with 'Removed user'
    for channel in store['channels']:
        if check_user_is_member(u_id, channel, 'all_members'):
            channel_leave_v1(u_id, channel['channel_id'])
            replace_messages(u_id, channel)
    
    # remove user from all dms, replace their messages with 'Removed user'
    for dm in store['dms']:
        if check_user_is_member(u_id, dm, 'members'):
            dm_leave_v1(u_id, dm['dm_id'])
            replace_messages(u_id, dm)

    # change the user's first name to 'Removed' and last name to 'user'
    user_data['first'] = 'Removed'
    user_data['last'] = 'user'

    # remove all current valid token info associated with the user being removed
    for token_data in store['tokens']:
        if token_data['user_id'] == u_id:
            store['tokens'].remove(token_data)
    
    user_data['removed'] = True
    
    data_store.set(store)

def change_permission(auth_user_id, permission_id):
    """
    helper function for admin_userpermission_change: replaces the messages in a
    given channel or dm with 'Removed user'

    Arguments:
        auth_user_id (int)  - an int representing a user
        permission_id (int) - an int representing a user permission

    Exceptions: N/A

    Return Value: N/A
    """

    store = data_store.get()
    for user in store['users']:
        if user['id'] == auth_user_id:
            user['perm_id'] = permission_id
    data_store.set(store)

def replace_messages(u_id, data):
    """
    helper function for admin_user_remove: replaces the messages in a given
    channel or dm with 'Removed user'

    Arguments:
        u_id (int)  - an int representing a user
        data (dict) - a channel or dm dict

    Exceptions: N/A

    Return Value: N/A
    """

    for message in data['messages']:
        if message['u_id'] == u_id:
            message['message'] = 'Removed user'
