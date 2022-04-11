'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

"""
Our Implementation:
data = {
    'users' = [{
        'id': 1,
        'email': 'abc@def.com',
        'pw': 'password',
        'first': 'first',
        'last': 'last',
        'handle': 'firstlast',
        'perm_id': 1,
        'removed': False,
        'profile_img_url': None, #For any given user, if they have yet to upload an image, 
                                    there should be a site-wide default image used.
    }],
    'tokens' = [{
        'user_id': user_data['id'],
        'session_id': SESSION_ID_COUNTER,
        'token': token,
    }],
    'channels' = [{
        'channel_id': 1,
        'name': 'channel_name',
        'owner_members': [{
            'u_id': 1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast',
        }],
        'all_members': [{
            'u_id': 1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast',
        }],
        'is_public': is_public,
        'messages' = [{
            'message_id': 1,
            'u_id': 1,
            'message': 'hewwo',
            'time_sent': utc_timestamp,
            'reacts': [{
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            }],
            'is_pinned': False
        }],
    }],
    'dms': [{
        'dm_id': 1,
        'name': 'dm_name',
        'creator': {
            'u_id': 1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast',
        },
        'members': [{
            'u_id': 1,
            'email': 'abc@def.com',
            'name_first': 'first',
            'name_last': 'last',
            'handle_str': 'firstlast',
        }],
        'messages' = [{
            'message_id': 1,
            'u_id': 1,
            'message': 'hewwo',
            'time_sent': utc_timestamp,
            'reacts': [{
                'react_id': 1,
                'u_ids': [],
                'is_this_user_reacted': False
            }],
            'is_pinned': False
        }],
    }]
}
"""

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'tokens': [],
    'channels': [],
    'dms': [],
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

## YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()
