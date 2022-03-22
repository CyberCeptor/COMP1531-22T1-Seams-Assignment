
from src.error import InputError, AccessError
from src.data_store import data_store
from src.token import token_valid_check
from src.other import check_valid_auth_id


def user_profile_v1(token, u_id):
    """
    For a valid user, returns information about their user_id, firstname,
    last name, and handle
    """
    # check the token is valid
    token_valid_check(token)
    check_valid_auth_id(u_id)

    valid = True
    # check the user_id is valid
    try:
        check_valid_auth_id(u_id)
    except InputError:
        valid = False
    if not valid:
        raise InputError("Invalid id")

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