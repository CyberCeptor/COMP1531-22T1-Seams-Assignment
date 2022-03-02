from src.error import InputError
from src.error import AccessError
from src.data_store import data_store


def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }





#  Given a channel with ID channel_id that the authorised user is a member of
#  provide basic details about the channel.
def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()
    channel = []
    # see if user is authorised
    user = search_user(auth_user_id)
    if user is None:
        raise InputError("Not an authorised user.")

    channel = search_channel(auth_user_id, channel_id)

    if channel is True:
        raise AccessError("Authorised user is not a member of the channel.")
    elif channel is False:
        raise InputError("Channel id does not have a valid channel associated with.")
    else:
        return{
            "name": channel['name'],
            "is_public": channel['is_public'],
            "owner_members": channel['owner_members'],
            "all_members": channel['all_members'],
        }

# return { name, is_public, owner_members, all_members }
 
# helper to see if the authorised user is a member of the channel
def search_channel(auth_user_id, channel_id):
    store = data_store.get()
    valid = True
    channels = store['channels']
    for channel in channels:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if channel['all_members'] == auth_user_id:
                    return channel
            # channel is valid but user is not a member of the provided channel
            return valid
    # channel_id does not refer to a valid channel
    valid = False     
    return valid

#helper function to see if user is in the data base
def search_user(auth_user_id):
    store = data_store.get()
    users = store['users']
    for user in users:
        if user['id'] == auth_user_id:
            return user
    return None




def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    return {
    }
