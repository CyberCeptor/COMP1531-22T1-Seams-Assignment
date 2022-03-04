from src.error import InputError
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
    if type(auth_user_id) != int:
        raise InputError('User id is not of a valid type')

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

def check_valid_channel_id(channel_id):
    """ checks if the given auth_user_id exists by checking if it is larger than
    0 and if it is found in the stored channel data """
    if type(channel_id) != int:
        raise InputError('Channel id is not of a valid type')

    if channel_id < 1:
        raise InputError('The channel id is not valid (out of bounds)')
    
    store = data_store.get()
    channel_exists = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            channel_exists = True

    # if the auth_user_id is not found, raise an AccessError
    if channel_exists == False:
        raise InputError('Channel does not exist in channels database')

# helper to see if the authorised user is a member of the channel
def check_user_is_member(auth_user_id, channel_id):
    store = data_store.get()
    user_is_member = False
    channel = store['channels'][channel_id - 1]
    for member in channel['all_members']:
        if member == auth_user_id:
            user_is_member = True

    return user_is_member