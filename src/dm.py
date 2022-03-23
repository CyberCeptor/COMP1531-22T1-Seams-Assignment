from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id
from src.error import InputError, AccessError
def dm_create_v1(token, u_ids):
    #get the data in data_store
    store = data_store.get()
    token_valid_check(token)
    auth_id = token_get_user_id(token)
    user_info = check_valid_auth_id(auth_id)
    # Assume the dm id start at 1 and increase by adding 1
    # for any newdm created
    dm_id = len(store['dms']) + 1
    
    # Assume the new message id starts at 1 and increase by adding 1
    # for any new message created
    current_message_id = 0
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] > current_message_id:
                current_message_id = message['message_id']
    new_message_id = current_message_id + 1
    name_list = []
    all_member_list = []
    
    for u_id in u_ids:
        if(u_ids.count(u_id) > 1):
            raise InputError('There are duplicate u_ids')
        user = check_valid_auth_id(u_id)
        name_list.append(user['handle'])
        all_member_list.append(user)
    all_member_list.append(user_info)
    
    #sort name list
    name_list.sort()
    #use , to separate
    dm_name = ",".join(name_list)

    new_dm = {
        'channel_id': -1, #assume a default value
        'name': dm_name,
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
    store['dms'].append(new_dm)
    # Save data
    data_store.set(store)
    
    return {'dm_id': dm_id}