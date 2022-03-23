"""
Filename: admin.py

Author: Aleesha, z5371516
Created: 22/03/22

Description: implementation for
    - changing the permission of a specified user
    - helper functions for the above
"""

from src.data_store import data_store

from src.other import check_valid_auth_id

from src.token import token_valid_check, token_get_user_id

from src.error import AccessError, InputError

def check_user_is_global_owner(auth_user_id):
    store = data_store.get()
    for user in store['users']:
        if user['id'] == auth_user_id and user['perm_id'] == 1:
            return True
    return False

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
