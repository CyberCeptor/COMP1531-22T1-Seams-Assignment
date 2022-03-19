"""
    Doc String == e.
"""
import jwt
import datetime
from src.error import InputError, AccessError
from src.data_store import data_store
# from flask import jsonify

SECRET = 'hotpot'
SESSION_ID_COUNTER = 0

def token_new_session_id():
    global SESSION_ID_COUNTER
    SESSION_ID_COUNTER += 1
    return SESSION_ID_COUNTER

# called when a user logs in and registers.
def token_generate(user_data):
    id = user_data['id']
    token = jwt.encode({'id': id}, SECRET, algorithm='HS256')
    # validate the new token created, if not raises an Error.
    token_valid_check(user_data, token)
    token_dict = {
        'user_id': user_data['id'],
        'session_id': SESSION_ID_COUNTER,
        'token': token,
        'time': datetime.datetime.now(),
    }

    store = data_store.get()
    store['tokens'].append(token_dict)
    data_store.set(store)

    # checks that the token has been added to the data_store.
    # if token_check_exists(token) == False:
    #     raise AccessError('Token not found in data_store')

    return token_dict

# given a token, returns the user_id
def token_get_user_id(token):
    decoded = jwt.decode(token, SECRET, algorithm=['HS256'])
    return int(decoded['user_id'])


# given a token, returns True if the token is < 24 hours old, otherwise False and removes the token from the data_store
def token_check_time_frame(token):
    decoded = jwt.decode(token, SECRET, algorithm=['HS256'])
    token_lifetime = datetime.now() - decoded['time']
    if token_lifetime.days == 0:
        return True
    token_remove(token)
    return False

# given a token, validate that the token exists in the tokens diction in data_store
def token_check_exists(token):
    store = data_store.get()
    for stored_token in store['tokens']:
        if stored_token['token'] == token:
            return True
    return False

# iterates through the token dictionary, and returns the dict of the token given.
def token_locate_in_data_store(token):
    store = data_store.get()
    for stored_token in store['tokens']:
        if stored_token['token'] == token:
            return stored_token
    return False

# when the token is older then 24hr, remove from the datastore dict list.
def token_remove(token):
    token_to_remove = token_locate_in_data_store(token)
    if token_to_remove:
        store = data_store.get()
        store['tokens'].remove(token_to_remove)
        data_store.set(store)
        return True
    raise AccessError('Token not found.')


# checks that the created token matches the user information in their dictionary.
def token_valid_check(user_data, token):
    jwt.decode(token, SECRET, algorithm=['HS256'])
    return True

def token_check_type(token):    
    if isinstance(token, str) is not True or type(token) is bool:
        raise InputError('Invalid token')
