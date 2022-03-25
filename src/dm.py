from src.other import check_valid_auth_id, get_messages, cast_to_int_get_requests
from src.token import token_valid_check, token_get_user_id
from src.error import InputError
from src.data_store import data_store

def dm_messages(token, dm_id, start):
    """
    check if given user id and channel id are valid,
    check start not overflow in channel,
    return messages to a channel authorised user,
    if too much messages do pagination operate.

    Arguments:
        auth_user_id (int)    - an integer that specifies user id
        channel_id (int) - an integer that specifies channel id
        start (int) - an integer that specifies index for message

    Exceptions:
        AccessError - Occurs if the user id does not exist in channel

    Return Value:
        Returns a dictionary containing message_id, u_id, message, time_sent,
        start and end if given user id and channel id are valid
    """
    token_valid_check(token)
    auth_user_id = token_get_user_id(token)

    # see if given auth_user_id and channel_id are valid
    check_valid_auth_id(auth_user_id)
    dm_data = check_valid_dm_id(dm_id)

    get_messages(auth_user_id, dm_data, start, "dm")

def check_valid_dm_id(dm_id):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: token
               u_ids

    Exceptions: InputError - raised by duplicate ids
                InputError - raised by invalid ids

    Return Value: dm_id
    """
    if type(dm_id) is bool:
        raise InputError('dm id is not of a valid type')

    dm_id = cast_to_int_get_requests(dm_id, 'dm id')

    if dm_id < 1:
        raise InputError('The dm id is not valid (out of bounds)')

    store = data_store.get()
    for dm in store['dms']:
       if dm['dm_id'] == dm_id:
            return dm
    # if the dm_id is not found, raise an AccessError
    raise InputError('dm does not exist in dms')
