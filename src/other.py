from src.error import AccessError

from src.data_store import data_store

def clear_v1():
    """ clears the stored data """
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    data_store.set(store)

def check_valid_auth_id(auth_user_id):
    """ checks if the given auth_user_id exists by checking if it is larger than
    0 and if it is found in the stored user data """
    if auth_user_id < 1:
        raise AccessError('The user id is not valid (out of bounds)')
    
    store = data_store.get()
    user_exists = False
    for user in store['users']:
        if user['id'] == auth_user_id:
            user_exists = True

    # if the auth_user_id is not found, raise an AccessError
    if user_exists == False:
        raise AccessError('User does not exist in users database')


def check_if_the_user_is_in_a_channel(auth_user_id):
    store = data_store.get()
    user_is_in_a_channel = False

    for channels in store['channels']:
        for members in channels['all_members']:
            if members == auth_user_id:
                user_is_in_a_channel = True


    if user_is_in_a_channel == False:
        raise AccessError('Channel does not exist in the channels database')
    
