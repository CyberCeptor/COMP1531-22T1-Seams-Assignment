
import jwt, datetime
from src.error import InputError, AccessError
from src.data_store import data_store


TOKEN_CODE = 'hotpot'
algorithm = 'HS256'
SESSION_ID_COUNTER = 0



def token_new_session_id():
    global SESSION_ID_COUNTER
    SESSION_ID_COUNTER += 1
    return SESSION_ID_COUNTER

# called when a user logs in and registers.
def token_generate(user_data):
    session_id = token_new_session_id()
    token = jwt.encode({'id': user_data['id'], 'session_id': session_id, 'handle': user_data['handle'], 'time': datetime.datetime.now()}, TOKEN_CODE, algorithm=algorithm)
    
    token_dict = {
        'user_id': user_data['id'],
        'session_id': SESSION_ID_COUNTER,
        'token': token,
        'time': datetime.datetime.now(),
    }

    store = data_store.get()
    store['tokens'].append(token_dict)
    data_store.set(store)
    return token_dict

# given a token, returns the user_id
def token_get_user_id(token):
    decoded = jwt.decode(token, TOKEN_CODE, algorithm)
    return int(decoded['user_id'])

# given a token, returns True if the token is < 24 hours old, otherwise False.
def token_check_time_frame(token):
    decoded = jwt.decode(token, TOKEN_CODE, algorithm)
    token_lifetime = datetime.datetime.now() - decoded['time']
    if token_lifetime.days == 0:
        return True
    return False

# given a token, validate that the token exists in the tokens diction in data_store
def token_check_exists(token):
    store = data_store.get()
    for stored_token in store['token']:
        if token == stored_token:
            return True
    return False

# when the token is older then 24hr, remove from the datastore dict list.
def token_expired(token):
    return

# checks that the created token matches the user information in their dictionary.
def token_valid_check(user_data, token):
    decoded = jwt.decode(token, TOKEN_CODE, algorithm)
    if decoded['id'] != user_data['id']:
        raise InputError('Incorrect id in token')
    if decoded['session_id'] != user_data['session_id']:
        raise InputError('Incorrect session id in token')
    if decoded['handle'] != user_data['handle']:
        raise InputError('Incorrect handle in token')
    if token_check_time_frame(token) == False:
        raise InputError('Token has expired')




