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
        'profile_img_url': user_profile_picture_default(u_id),
        'reset_code': None,
        'users_stats: {
            'channels_joined': [
                {
                    'num_channels_joined': 0,
                    'time_stamp': 01234567
                },
                {
                    'num_channels_joined': 1,
                    'time_stamp': 12345678
                }
            ],
            'dms_joined': [
                {
                    'num_dms_joined': 0,
                    'time_stamp': 01234567,
                },
                {
                    'num_dms_joined': 1,
                    'time_stamp': 12345678,
                }
            ],
            'involvement_rate': 1.0,
            'messages_sent': [
                {
                    'num_messages_sent': 0,
                    'time_stamp': 01234567
                },
                {
                    'num_messages_sent': 1,
                    'time_stamp': 12345678
                }
            ]
        }
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
            'is_pinned': False,
            'standup': {
                'is_active': False,
                'time_finish': None,
                'messages_buffer': [],
            },
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
    }],
    'workspace_stats': {
        'channels_exist': [
        {
                'num_channels_exist': 0,
                'time_stamp': 012345
        },
        {
                'num_channels_exist': 1,
                'time_stamp': 123456
        }
    ], 
        'dms_exist': [
        {
                'num_dms_exist': 0,
                'time_stamp': 01234
        },
        {
                'num_dms_exist': 1,
                'time_stamp': 12345
        }
    ], 
        'messages_exist': [
        {
            'num_messages_exist': 0,
            'time_stamp': 01234
        },
        {
            'num_messages_exist': 1,
            'time_stamp': 12345
        }
    ], 
        'utilization_rate': 1.0,
    }
}
"""

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'tokens': [],
    'channels': [],
    'dms': [],
    'workspace_stats': {
        'channels_exist': [],
        'dms_exist': [],
        'messages_exist': [],
        'utilization_rate': 0,
    },
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
