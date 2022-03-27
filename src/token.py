"""
    Doc String == e.
"""
import jwt
import datetime
from src.error import InputError, AccessError
from src.data_store import data_store

from src.global_vars import new_id

# from flask import jsonify

key = 'hotpot'
algorithm = 'HS256'

# called when a user logs in and registers.
def token_generate(user_data):
    id = user_data['id']
    session_id = new_id('session')
    expiry_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    handle = user_data['handle']
    token = jwt.encode({'id': id, 'session_id': session_id, 'handle': handle,
                        'exp': expiry_time}, key, algorithm)

    token_dict = {
        'user_id': user_data['id'],
        'session_id': session_id,
        'token': token,
    }

    store = data_store.get()
    store['tokens'].append(token_dict)
    data_store.set(store)

    return token

def token_get_user_id(token):
    """
    returns the user_id encoded into the given valid token

    Arguments:
        token (str) - a valid jwt token string

    Exceptions: N/A

    Return Value: Returns the user id of the user that the token belongs to
    """

    decoded = jwt.decode(token, key, algorithm)
    return int(decoded['id'])

def token_locate_in_data_store(token):
    """
    iterates through the token dictionary and returns the dict of the token
    given if it is found

    Arguments:
        token (str) - a valid jwt token string

    Exceptions:
        AccessError - Raised if token cannot be found in the tokens data

    Return Value: Returns the dict of the stored token if it is found
    """

    store = data_store.get()
    for stored_token in store['tokens']:
        if stored_token['token'] == token:
            return stored_token
    raise AccessError('Invalid token')

def token_remove(token):
    """
    remove a token from the tokens data if it is expired or if a user logs out

    Arguments:
        token (str) - a valid jwt token string

    Exceptions:
        AccessError - Raised if token is not saved in the tokens data

    Return Value: N/A
    """

    token_to_remove = token_locate_in_data_store(token)
    store = data_store.get()
    store['tokens'].remove(token_to_remove)
    data_store.set(store)

def token_valid_check(token):
    """
    checks that the passed in token is of a valid type, is not expired, is a
    valid jwt token string, and is stored in the tokens data

    Arguments:
        token (str) - a jwt token string

    Exceptions:
        InputError  - Raised if token is of an invalid type
        AccessError - Raised if token is expired, is not a valid jwt token
                      string, and is not saved in the tokens data

    Return Value: N/A
    """

    # invalid input types for tokens
    if token in ['True', 'False', '']:
        raise InputError('Invalid token')

    # if the token can be casted to an int, it is of the wrong type
    try:
        token = int(token)
        raise InputError('Invalid token')
    except ValueError:
        pass

    valid = True
    error_message = ''
    # decode will check the current time against the expiry time
    try:
        jwt.decode(token, key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        # remove the token if it is expired
        valid = False
        error_message = 'Token has expired'
        token_remove(token)
    except jwt.DecodeError:
        # a string has been passed in but it's not a jwt token string or it's a
        # normal string
        valid = False
        error_message = 'Invalid token'

    # return the appropriate error message
    if not valid:
        raise AccessError(error_message)

    # check if the valid token is stored in the data
    token_locate_in_data_store(token)
