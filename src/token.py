"""
    Doc String == e.
"""
import jwt
import datetime
from src.error import InputError, AccessError
from src.data_store import data_store
# from flask import jsonify

KEY = 'hotpot'
ALGORITHM = 'HS256'
SESSION_ID_COUNTER = 0

def token_new_session_id():
    global SESSION_ID_COUNTER
    SESSION_ID_COUNTER += 1
    return SESSION_ID_COUNTER

def reset_session_id():
    global SESSION_ID_COUNTER
    SESSION_ID_COUNTER = 0
    return SESSION_ID_COUNTER

# called when a user logs in and registers.
def token_generate(user_data):
    id = user_data['id']
    session_id = token_new_session_id()
    expiry_time = datetime.datetime.now() + datetime.timedelta(hours=24)
    handle = user_data['handle']
    token = jwt.encode({'id': id, 'session_id': session_id, 'handle': handle, 'exp': expiry_time}, KEY, ALGORITHM)

    token_dict = {
        'user_id': user_data['id'],
        'session_id': session_id,
        'token': token,
    }

    store = data_store.get()
    store['tokens'].append(token_dict)
    data_store.set(store)

    return token

# given a token, returns the user_id
def token_get_user_id(token):
    decoded = jwt.decode(token, KEY, ALGORITHM)
    return int(decoded['id'])

# iterates through the token dictionary, and returns the dict of the token given.
def token_locate_in_data_store(token):
    store = data_store.get()
    for stored_token in store['tokens']:
        if stored_token['token'] == token:
            return stored_token
    raise AccessError('Invalid token')

# if the token is older then 24hours old, or the user logs out, the token is removed.
def token_remove(token):
    token_to_remove = token_locate_in_data_store(token)
    store = data_store.get()
    store['tokens'].remove(token_to_remove)
    data_store.set(store)

# checks that the created token matches the user information in their dictionary.
def token_valid_check(token):
    # decode will check the current time againest the expiry time
    try:
        token = int(token)
        raise InputError('Invalid token')
    except ValueError:
        pass

    if token == 'True' or token == 'False':
        raise InputError('Invalid token')

    if token == '':
        raise InputError('Invalid token')

    valid = True
    error_message = ''
    try:
        jwt.decode(token, KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        valid = False
        error_message = 'Token has expired'
        token_remove(token)
    except jwt.DecodeError:
        valid = False
        error_message = 'Invalid token'

    if not valid:
        raise AccessError(error_message)
    token_locate_in_data_store(token)
