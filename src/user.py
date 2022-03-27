from src.data_store import data_store
from src.token import token_valid_check, token_locate_in_data_store, token_get_user_id
from src.other import check_valid_auth_id, cast_to_int_get_requests
from src.auth import check_invalid_email
from src.error import InputError

VALID_EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'


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

"""
Update the authorised user's first and last name
PUT
Arguments:
    -   token
    -   name_first
    -   name_last
Exceptions:
    InputError:
        -   length of name_first is not between 1 and 50 characters inclusive
        -   length of name_last is not between 1 and 50 characters inclusive
Return Value:
    N/A

"""

def user_profile_setname_v1(token, name_first, name_last):

    
    return {}











"""
Update the authorised user's email address

PUT

    InputError:
        - email entered is not a valid email
        - email address is already used by another user
"""
def user_profile_setemail_v1(token, email):
    store = data_store.get()

    # check the email is valid (i.e. usable email address, format)
    # check that the email isn't already used by another user
    # both done by check_invalid_email.
    # need to check that the email is the correct format.

    check_invalid_email(store, VALID_EMAIL_REGEX, str(email))

    # check the token is current and acceptable
    token_valid_check(token)
    token_locate_in_data_store(token)
    user_id = token_get_user_id(token)

    # set the user email to the new email
    for user in store['users']:
        if user['id'] == user_id:
            user['email'] = email

    # iterate through all channels that the member is in and set 
    # the email there aswell.

    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['email'] = email
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['email'] = email

    data_store.set(store)
    return {}
