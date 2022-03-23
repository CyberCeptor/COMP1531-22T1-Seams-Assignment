from operator import index
from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id
from src.error import InputError, AccessError
def dm_create_v1(token, u_ids):
    #get the data in data_store
    store = data_store.get()
    token_valid_check(token)
    auth_id = token_get_user_id(token)
    for user in store['users']:
        if user['id'] == auth_id:
            user_info = user

    #check the duplicate ids in u_ids
    check_duplicate_id(u_ids)
    
    # Assume the dm id start at 1 and increase by adding 1
    # for any newdm created
    current_id = 0
    for channel in store['channels']:
        if channel['dm_id'] > current_id:
            current_id = channel["dm_id"]
    dm_id = current_id + 1
    
    # Assume the new message id starts at 1 and increase by adding 1
    # for any new message created
    current_message_id = 0
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] > current_message_id:
                current_message_id = message['message_id']
    new_message_id = current_message_id + 1
    
    #copy the u_ids list
    new_u_ids = u_ids.copy()
    #add the user who sent dm in new list
    new_u_ids.append(auth_id)
    name_list = []
    #add the handle in name list
    for id in new_u_ids:
        for user in store['users']:
            if id == user['id']:
                name_list.append(user['handle'])
                break
    #sort name list
    name_list.sort()
    #use , to separate
    dm_name = ",".join(name_list)
    #the user creates the dm is the owner
    owner_list = [{
        'u_id': user_info['id'],
        'email': user_info['email'],
        'name_first': user_info['first'],
        'name_last': user_info['last'],
        'handle_str': user_info['handle']
    }]
    
    #create a all_member list to show all the members in dm including the owner
    all_member_list = []
    owner = {
        'u_id': user_info['id'],
        'email': user_info['email'],
        'name_first': user_info['first'],
        'name_last': user_info['last'],
        'handle_str': user_info['handle']
    }
    #add the owner
    all_member_list.append(owner)
    #add the other members
    for other in u_ids:
        for user1 in store['users']:
            if user1['id'] == other:
                user_info1 = user1
                other_user = {
                    'u_id': user_info1['id'],
                    'email': user_info1['email'],
                    'name_first': user_info1['first'],
                    'name_last': user_info1['last'],
                    'handle_str': user_info1['handle']
                }
                all_member_list.append(other_user)

    new_dm = {
        'channel_id': -1, #assume a default value
        'name': dm_name,
        'owner_members': owner_list,
        'all_members': all_member_list,
        'is_public': False, # Assume false because it is a dm
        'dm_id': dm_id,
        'messages': [
            {
                'message_id' : new_message_id, # Assume it is greater than 0
                'message' : "",
                'timestamp' : 0,
                'auth_user_id' : auth_id
            }

        ]

    }
    # Add the dm channel to channels
    store['channels'].append(new_dm)
    # Save data
    data_store.set(store)
    
    return {'dm_id': dm_id}

#create a function to check duplicate id in u_ids
def check_duplicate_id(u_ids):
    length_uids = len(u_ids)
    index = 0
    for id in u_ids:
        check_valid_auth_id(id)
        index += 1
        if(index < length_uids):
            if(id == u_ids[index]):
                raise InputError('There are duplicate u_ids')








   