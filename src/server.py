import sys
import signal

import pickle

from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError, AccessError
from src.token import token_remove, token_valid_check, reset_session_id
from src import config

from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

data_store = {}
try:
    data_store = pickle.load(open('datastore.p'), 'rb')
except Exception:
    pass

def get_data():
    global data_store
    print(data_store)
    return data_store

def save_data():
    data_store = get_data()
    with open('datastore.p', 'wb') as FILE:
        pickle.dump(data_store, FILE)

# Example
# http://127.0.0.1:1337/hello
# body -> hewwo!
@APP.route('/hello', methods=['POST'])
def hello():
    return "hewwo!"

# http://127.0.0.1:1337/echo?data=hi
# body -> {"data":hi}
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route('/auth/register/v2', methods=['POST'])
def register():
    data = request.get_json()
    user = auth_register_v1(data['email'], data['password'],
                            data['name_first'], data['name_last'])
    data_store = get_data()
    print(data_store)
    return dumps({
        'token': user['token'],
        'auth_user_id': user['auth_user_id']
    })

@APP.route('/auth/login/v2', methods=['POST'])
def login():
    data = request.get_json()
    user = auth_login_v1(data['email'], data['password'])
    data_store = get_data()
    print(data_store)
    return dumps({
        'token': user['token'],
        'auth_user_id': user['auth_user_id']
    })

@APP.route('/auth/logout/v1', methods=['POST'])
def logout():
    data = request.get_json()
    token = data['token']
    print(token)
    token_valid_check(token)
    token_remove(token)
    data_store = get_data()
    print(data_store)
    return dumps({})

@APP.route('/users/all/v1', methods=['GET'])
def get_users():
    token = request.args.get('token')
    token_valid_check(token)
    to_return = []
    for user in data_store['users']:
        to_return.append({
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['first'],
            'name_last': user['last'],
            'handle_str': user['handle'],
        })
    return dumps({
        'users': to_return
    })

@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    clear_v1()
    reset_session_id()
    data_store = get_data()
    print(data_store)
    return dumps({})

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port, debug=True) # Do not edit this port
