"""
Filename: dm.py

Author: Zefan Cao(z5237177), Xingjian Dong (z5221888)
Created: 14/03/2022 - 24/03/2022

Description: implementation for
    - create a dm with token and u_ids
    - list and give the details of this dm
    - remove and leave with given token
    - helper functions for the above
"""
from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id, cast_to_int_get_requests, check_user_is_member, get_messages
from src.error import InputError, AccessError
from src.global_vars import new_id
from src.data_store import data_store

def dm_create_v1(token, u_ids):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: token (str)          - unique str representation of user
               u_ids (str)          - the list of u_id

    Exceptions: InputError - raised by duplicate ids
                InputError - raised by invalid ids

    Return Value: dm_id(int)            -unique int represent no. of dm
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
    store['dms'].append(new_dm)
    # Save data
    data_store.set(store)

    return {'dm_id': dm_id}

def dm_list_v1(token):
    """
    clears any data stored in data_store and registers users with the
    given information, list the dm info with token

    Arguments: token (str)          - unique str representation of user

    Exceptions: InputError - raised by wrong token

    Return Value: dms(dic)            -a dic including dm id and name
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
    given information, remove dm with token and dm id

    Arguments: token (str)          - unique str representation of user
               dm_id(int)           - unique int represent no. of dm

    Exceptions: InputError - raised by wrong token
                InputError - raised by wrong dm_id
                AccessError - raised by user is not a crator
                AccessError - raised by user no longer in dm

    Return Value: N/A
    """
    store = data_store.get()
    token_valid_check(token)
    dm = check_valid_dm_id(dm_id)
    auth_id = token_get_user_id(token)

    if check_user_is_member(auth_id, dm, 'members') is None:
        raise AccessError('The authorised user is no longer in dm')
    
    if dm['creator']['u_id'] != auth_id:
        raise AccessError('The auth user is not original dm creator')
    else:
        store['dms'].remove(dm)
    
    data_store.set(store)

def dm_details_v1(token, dm_id):
    """
    clears any data stored in data_store and registers users with the
    given information, show dm details with token and dm id

    Arguments: token (str)          - unique str representation of user
               dm_id(int)           - unique int represent no. of dm

    Exceptions: InputError - raised by wrong token
                InputError - raised by wrong dm_id
                AccessError - raised by user no longer in dm

    Return Value: a dic             -including name and members
    """
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
    """
    clears any data stored in data_store and registers users with the
    given information, show dm details with token and dm id

    Arguments: auth_user_id (int)          - unique int representation of user
               dm_id(int)           - unique int represent no. of dm

    Exceptions: InputError - raised by wrong token
                InputError - raised by wrong dm_id
                AccessError - raised by user no longer in dm

    Return Value: a dic             -including name and members
    """
    dm = check_valid_dm_id(dm_id)
    store = data_store.get()

    if(dm['creator']['u_id'] == auth_user_id):
        dm['creator'] = {}

    member = check_user_is_member(auth_user_id, dm, 'members')
    if member is None:
        raise AccessError('The authorised user is no longer in dm')
    else:
        dm['members'].remove(member)
        data_store.set(store)


def check_valid_dm_id(dm_id):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: token (str)          - unique str representation of user
               u_ids (str)          - the list of u_id

    Exceptions: InputError - raised by duplicate ids
                InputError - raised by invalid ids

    Return Value: dm
    """
    if type(dm_id) is bool:
        raise InputError('dm id is not of a valid type')

    dm_id = cast_to_int_get_requests(dm_id, 'dm id')

    if dm_id < 1:
        raise InputError('The dm id is not valid (out of bounds)')

    store = data_store.get()
    
    for dm in store['dms']:
       if dm['dm_id'] == dm_id:
            return dm
    # if the dm_id is not found, raise an AccessError
    raise InputError('dm does not exist in dms')

def check_creator_notin_u_ids_duplicate(u_id, id, u_ids):
    """
    check the whether there is duplicate ids and whether the creator is in uids

    Arguments: u_id (int)          - unique str representation of user
               u_ids (str)          - the list of u_id

    Exceptions: InputError - raised by creator in u_ids
                InputError - raised by duplicate ids

    Return Value: N/A
    """
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
        auth_user_id (int) - an integer that specifies user id
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
