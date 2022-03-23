from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id
from src.error import InputError, AccessError
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
    dm_id = len(store['dms']) + 1
    creator_list = []
    name_list = []
    all_member_list = []
    all_member_list.append(owner)
    name_list.append(user_info['handle'])
    creator_list.append(owner)
    for u_id in u_ids:
        if(u_ids.count(u_id) > 1):
            raise InputError('There are duplicate u_ids')
        user = check_valid_auth_id(u_id)
        user1 = {
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['first'],
            'name_last': user['last'],
            'handle_str': user['handle']
        }
        name_list.append(user['handle'])
        all_member_list.append(user1)
    #sort name list
    name_list.sort()
    #use , to separate
    dm_name = ",".join(name_list)

    new_dm = {
        'name': dm_name,
        'members': all_member_list,
        'dm_id': dm_id,
        'creator': creator_list,
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
    auth_id = token_get_user_id(token)
    dm_list = []
    store = data_store.get()
    for dm in store['dms']:
        for member in dm['members']:
            if auth_id == member['u_id']:
                new_dict = {"dm_id": dm['dm_id'], "name": dm['name']}
                dm_list.append(new_dict)

    return {"dms": dm_list}