

from src.token import token_valid_check

from src.data_store import data_store

def users_all_v1(token):
    store = data_store.get()
    token_valid_check(token)

    to_return = []
    for user in store['users']:
        if user['first'] != 'Removed' and user['last'] != 'user':
            to_return.append({
                'u_id': user['id'],
                'email': user['email'],
                'name_first': user['first'],
                'name_last': user['last'],
                'handle_str': user['handle'],
            })

    return {
        'users': to_return
    }