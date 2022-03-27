"""
Filename: dm.py

Author: Zefan Cao(z5237177), Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: dm functions
"""
from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id, check_user_is_member, get_messages, check_valid_dm_id
from src.error import InputError, AccessError
from src.global_vars import new_id
from src.data_store import data_store

def dm_create_v1(token, u_ids):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: token
               u_ids

    Exceptions: InputError - raised by duplicate ids
                InputError - raised by invalid ids

    Return Value: dm_id
    """
    #get the data in data_store
    store = data_store.get()
    token_valid_check(token)
    auth_id = token_get_user_id(token)
    user_info = check_valid_auth_id(auth_id)
    owner = {
        'u_id': user_info['id'],
        'email': user_info['email'],
        'name_first': user_info['first'],
        'name_last': user_info['last'],
        'handle_str': user_info['handle']
    }
    # Assume the dm id start at 1 and increase by adding 1
    # for any newdm created
    dm_id = new_id('dm')
    name_list = []
    all_member_list = []
    all_member_list.append(owner)
    name_list.append(user_info['handle'])
    for u_id in u_ids:
        check_creator_notin_u_ids_duplicate(auth_id, u_id, u_ids)
        user = check_valid_auth_id(u_id)
        name_list.append(user['handle'])
        all_member_list.append({
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['first'],
            'name_last': user['last'],
            'handle_str': user['handle']
        })
    #sort name list
    name_list.sort()
    #use , to separate
    dm_name = ", ".join(name_list)

    new_dm = {
        'name': dm_name,
        'members': all_member_list,
        'dm_id': dm_id,
        'creator': owner,
        'messages': []
    }
    # Add the dm channel to channels
    store['dms'].append(new_dm)
    # Save data
    data_store.set(store)

    return {'dm_id': dm_id}

def dm_list_v1(token):
    """
    clears any data stored in data_store and registers a user with the
    given information, create the dm with token and u_ids, list with token

    Arguments: token

    Exceptions: N/A

    Return Value: N/A
    """
    token_valid_check(token)
    auth_id = token_get_user_id(token)
    dm_list = []
    store = data_store.get()
    for dm in store['dms']:
        check_user_is_member(auth_id, dm, 'members')
        new_dict = {
            "dm_id": dm['dm_id'], 
            "name": dm['name']
        }
        dm_list.append(new_dict)

    return {"dms": dm_list}

def dm_remove_v1(token, dm_id):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: token
               u_ids

    Exceptions: InputError - raised by duplicate ids
                InputError - raised by invalid ids

    Return Value: dm_id
    """
    store = data_store.get()
    token_valid_check(token)
    # Call helper function to check for valid dm
    dm = check_valid_dm_id(dm_id)

    # Call helper function to check valid token
    auth_id = token_get_user_id(token)

    if check_user_is_member(auth_id, dm, 'members') is None:
        raise AccessError('The authorised user is no longer in dm')
    
    if dm['creator']['u_id'] != auth_id:
        raise AccessError('The auth user is not original dm creator')
    else:
        store['dms'].remove(dm)
    
    data_store.set(store)

def dm_details_v1(token, dm_id):
    token_valid_check(token)
    auth_id = token_get_user_id(token)
    dm = check_valid_dm_id(dm_id)

    if check_user_is_member(auth_id, dm, 'members') is None:
        raise AccessError('The authorised user is no longer in dm')
    
    return {
        'name': dm['name'],
        'members': dm['members']
    }


def dm_leave_v1(auth_user_id, dm_id):
    dm = check_valid_dm_id(dm_id)
    store = data_store.get()

    if check_user_is_member(auth_user_id, dm, 'members') is None:
        raise AccessError('The authorised user is no longer in dm')

    if(dm['creator']['u_id'] == auth_user_id):
        dm['creator'] = {}

    for member in dm['members']:
        if(auth_user_id == member['u_id']):
            dm['members'].remove(member)
            data_store.set(store)

def check_creator_notin_u_ids_duplicate(u_id, id, u_ids):
    if u_id == id:
        raise InputError('Creator can not dm himself')
    elif(u_ids.count(id) > 1):
        raise InputError('There are duplicate u_ids')

def dm_messages_v1(token, dm_id, start):
    """
    check if given user id and dm id are valid,
    check start not overflow in dm,
    return messages to a dm authorised user,
    if too much messages do pagination operate.

    Arguments:
        auth_user_id (int)    - an integer that specifies user id
        dm_id (int) - an integer that specifies dm id
        start (int) - an integer that specifies index for message

    Exceptions:
        AccessError - Occurs if the user id does not exist in dm

    Return Value:
        Returns a dictionary containing message_id, u_id, message, time_sent,
        start and end if given user id and dm id are valid
    """
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # see if given auth_user_id and dm_id are valid
    check_valid_auth_id(auth_user_id)
    dm_data = check_valid_dm_id(dm_id)

    messages = get_messages(auth_user_id, dm_data, start, "dm")

    return messages
