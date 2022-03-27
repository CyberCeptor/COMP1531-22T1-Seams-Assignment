from src.token import token_valid_check

from src.data_store import data_store

def users_all_v1(token):
    """
    returns the data of every user in the stored data, excluding those who have
    been removed

    Arguments:
        token (str) - a valid jwt token string

    Exceptions: N/A

    Return Value:
        Returns a dict containing each users' u_id, email, name_first,
        name_last, and handle_str if the user has not been removed
    """

    store = data_store.get()
    token_valid_check(token)

    to_return = []
    for user in store['users']:
        # if the user has not been removed, return their data
        if user['removed'] is False:
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