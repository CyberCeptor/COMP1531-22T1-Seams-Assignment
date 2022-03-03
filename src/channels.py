from src.error import InputError
from src.other import check_valid_auth_id

from src.data_store import data_store





def channels_list_v1(auth_user_id):

    # looping threough data_store['channels']
    # search through 'all_members', when the auth_user_id occurs,
    # add the channel information to the new dict.
    # return new dict.




    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }







def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }




    # Creates a new channel with the given name and is either public or private.
    # The user who created it automatically joins it.
    # Returns the channel id.

def channels_create_v1(auth_user_id, name, is_public):
    # retrieving channel data from data_store
    store = data_store.get()

    check_valid_auth_id(auth_user_id)

    if len(name) > 20:
        raise InputError("Error: the channel name must be less than 20 characters.")

    if len(name) < 1:
        raise InputError("Error: no channel name was entered.")

    if type(is_public) != bool:
        raise InputError("Error: the public/private value given is not of type bool.")

    # Test channel names for repition, unless public vs private.
    # Loops through data_store['channels'] to check channel names if they already exist
    # and are of the same is_public (public/private) then cannot be created.
    # Having two channles with the same name is fine, as long as they have different is_public values.
    for channel in store['channels']:
        if channel['name'] == name and channel['is_public'] == is_public:
            raise InputError("This channel name already exists.")

    # get the number of channels created so far, incremented for the new channel id.
    channel_id = len(store['channels']) + 1

    # Storing the channel information 
    channel_data = {
        'channel_id': channel_id,
        'name': name,
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'is_public': is_public,
    }

    store['channels'].append(channel_data)
    

    return {
        'channel_id': channel_id
    }
