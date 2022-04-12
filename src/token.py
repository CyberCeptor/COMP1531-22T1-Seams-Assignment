"""
Filename: token.py

Author: Jenson Morgan(z5360181), Aleesha Bunrith(z5371516)
Created: 24/02/2022 - 27/03/2022

Description: implementation for
    - token generation
    - checking if a token is valid
    - locating token and associated data in the data store
    - getting the encoded user id from a token
    - removing a token and the associated stored data
"""

import jwt

import datetime

from datetime import timezone

from src.error import InputError, AccessError

from src.data_store import data_store

from src.global_vars import new_id, KEY, ALGORITHM

def token_generate(user_data):
    """
    generates a token using the user data passed in, a generated session id and
    an expiry time and saved associated details into the data store

    Arguments:
        user_data (dict) - a specific user dict from the data store

    Exceptions: N/A

    Return Value:
        Returns the newly generated token
    """

    id = user_data['id']
    session_id = new_id('session')
    expiry_time = datetime.datetime.now(tz=timezone.utc) + \
                  datetime.timedelta(hours=24)
    handle = user_data['handle']

    # encode the above data into a token
    token = jwt.encode({'id': id, 'session_id': session_id, 'handle': handle,
                        'exp': expiry_time}, KEY, ALGORITHM)

    # save token and associated details into a dict to be stored in the list of
    # token data
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
    returns the user_id encoded into the given valid token, assumes that we have
    checked if the token is valid

    Arguments:
        token (str) - a valid jwt token string

    Exceptions: N/A

    Return Value:
        Returns the user id of the user that the token belongs to
    """

    decoded = jwt.decode(token, KEY, ALGORITHM)
    return int(decoded['id'])

def token_locate_in_data_store(token):
    """
    iterates through the token dictionary and returns the dict of the token
    given if it is found

    Arguments:
        token (str) - a valid jwt token string

    Exceptions:
        AccessError - Raised if token cannot be found in the tokens data

    Return Value:
        Returns the dict of the stored token if it is found
    """

    store = data_store.get()
    for stored_token in store['tokens']:
        if stored_token['token'] == token:
            return stored_token
    raise AccessError(description='Invalid token')

def token_valid_check(function):
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
 
    def inner(*args, **kwargs):
        token_to_check = args[0]

        # invalid input types for tokens
        if token_to_check in ['True', 'False', '']:
            raise InputError(description='Invalid token')

        # if the token can be casted to an int, it is of the wrong type
        try:
            token_to_check = int(token_to_check)
            raise InputError(description='Invalid token')
        except ValueError:
            pass

        # if token can be successfully decoded with no errors, it is valid
        try:
            jwt.decode(token_to_check, KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise AccessError(description='Token has expired') from AccessError
        except jwt.DecodeError:
            raise AccessError(description='Invalid token') from InputError

        # check if the valid token is stored in the data
        token_locate_in_data_store(token_to_check)
        return function(*args, **kwargs)
    return inner

@token_valid_check
def token_remove(token):
    """
    remove a token from the tokens data if it is expired or if a user logs out

    Arguments:
        token (str) - a valid jwt token string

    Exceptions:
        AccessError - Raised if token is not saved in the tokens data

    Return Value: N/A
    """
    print('removing tokens')
    token_to_remove = token_locate_in_data_store(token)
    store = data_store.get()
    store['tokens'].remove(token_to_remove)
    print(store)
    data_store.set(store)
 