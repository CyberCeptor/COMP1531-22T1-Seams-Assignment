
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
    # check the user_id is valid
    valid = True
    try:
        u_id = int(u_id)
    except ValueError:
        valid = False
    if not valid:
        raise InputError("User id is not of correct type.")

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