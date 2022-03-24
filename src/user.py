from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import token_valid_check
from src.other import check_valid_auth_id, cast_to_int_get_requests

def user_profile_v1(token, u_id):
    """
    For a valid user, returns information about their user_id, firstname,
    last name, and handle
    """
    token_valid_check(token)
    u_id = cast_to_int_get_requests(u_id, 'user id')

    check_valid_auth_id(u_id)

    store = data_store.get()
    for users in store['users']:
        if users['id'] == u_id:
            user = {
                'u_id': users['id'],
                'email': users['email'],
                'name_first': users['first'],
                'name_last': users['last'],
                'handle_str': users['handle'],
            }

    return user