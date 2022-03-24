"""
Filename: admin.py

Author: Aleesha, z5371516
Created: 22/03/22

Description: implementation for
    - changing the permission of a specified user
    - helper functions for the above
"""

from src.data_store import data_store

from src.other import check_valid_auth_id, check_user_is_global_owner, check_user_is_member

from src.token import token_valid_check, token_get_user_id, token_remove

from src.error import AccessError, InputError

from src.channel import channel_leave_v1

def change_permission(auth_user_id, permission_id):
    store = data_store.get()
    for user in store['users']:
        if user['id'] == auth_user_id:
            user['perm_id'] = permission_id
    data_store.set(store)

def admin_userpermission_change(token, u_id, permission_id):
    store = data_store.get()

    token_valid_check(token)
    auth_user_id = token_get_user_id(token)
    if not check_user_is_global_owner(auth_user_id):
        raise AccessError(description='User is not a global owner')

    check_valid_auth_id(u_id)

    if not isinstance(permission_id, int) or type(permission_id) is bool:
        raise InputError('Permission id is not of valid type')

    if permission_id not in [1, 2]:
        raise InputError('Invalid permission id')

    num_global_owners = len([user for user in store['users'] if 
                             user['perm_id'] == 1])

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
    # for dm in store['dms']:
    #     if check_user_is_member(u_id, dm, 'members'):
    #         dm_leave_v1(token, dm['dm_id'])
    #         replace_messages(u_id, dm)

    # change the user's first name to 'Removed' and last name to 'user'
    user_data['first'] = 'Removed'
    user_data['last'] = 'user'

    # invalidate all current valid tokens associated with user being removed
    for token_data in store['tokens']:
        if token_data['user_id'] == u_id:
            token_remove(token_data['token'])
    
    user_data['removed'] = True
    
    data_store.set(store)

def replace_messages(u_id, data):
    """
    replaces the messages in a given channel or dm with 'Removed user'

    Arguments:
        u_id (int)  - an int representing a user
        data (dict) - a channel or dm dict

    Exceptions: N/A

    Return Value: N/A
    """

    for message in data['messages']:
        if message['u_id'] == u_id:
            message['message'] = 'Removed user'
