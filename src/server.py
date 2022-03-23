import sys
import signal
import pickle
from src import config
from json import dumps
from flask import Flask, request
from flask_cors import CORS

from src.auth import auth_register_v2, auth_login_v2
from src.user import user_profile_v1

from src.error import InputError
from src.token import token_remove, token_valid_check
from src.admin import admin_userpermission_change
from src.other import clear_v1

from src.channel import channel_details_v2, channel_invite_v2
from src.channel import channel_join_v2, channel_messages_v2, channel_leave_v1
from src.channels import channels_create_v2
from src.channels import channels_list_v2, channels_listall_v2

from src.data_store_pickle import pickle_data

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

pickle_data()

DATA_STORE = {}

def get_data():
    global DATA_STORE
    try:
        DATA_STORE = pickle.load(open('datastore.p', 'rb'))
    except Exception:
        pass
    return DATA_STORE

################################################################################
##                              AUTH ROUTES                                   ##
################################################################################

@APP.route('/auth/register/v2', methods=['POST'])
def register():
    data = request.get_json()
    user = auth_register_v2(data['email'], data['password'],
                            data['name_first'], data['name_last'])
    save_data()
    return dumps({
        'token': user['token'],
        'auth_user_id': user['auth_user_id']
    })

@APP.route('/auth/login/v2', methods=['POST'])
def login():
    data = request.get_json()
    user = auth_login_v2(data['email'], data['password'])
    save_data()
    return dumps({
        'token': user['token'],
        'auth_user_id': user['auth_user_id']
    })

@APP.route('/auth/logout/v1', methods=['POST'])
def logout():
    data = request.get_json()
    token = data['token']
    token_valid_check(token)
    token_remove(token)
    save_data()
    return dumps({})

################################################################################
##                              USERS ROUTES                                  ##
################################################################################

@APP.route('/users/all/v1', methods=['GET'])
def get_users():
    global DATA_STORE
    token = request.args.get('token')
    token_valid_check(token)
    to_return = []
    for user in DATA_STORE['users']:
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

################################################################################
##                              USER ROUTES                                   ##
################################################################################

@APP.route('/user/profile/v1', methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    profile = user_profile_v1(token, u_id)
    save_data()
    return dumps(profile)

################################################################################
##                              ADMIN ROUTES                                  ##
################################################################################

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def change_perms():
    data = request.get_json()
    token = data['token']
    admin_userpermission_change(token, data['u_id'], data['permission_id'])
    save_data()
    return dumps({})

################################################################################
##                             CHANNELS ROUTES                                ##
################################################################################

@APP.route("/channels/create/v2", methods=['POST'])
def channel_create():
    data = request.get_json()
    channel = channels_create_v2(data['token'], data['name'], data['is_public'])
    save_data()
    return dumps(channel)

@APP.route("/channels/list/v2", methods=['GET'])
def channel_list():
    token = request.args.get('token')
    channel_list = channels_list_v2(token)
    save_data()
    return dumps(channel_list)

@APP.route('/channels/listall/v2', methods=['GET'])
def channel_listall():
    token = request.args.get('token')
    channels_list = channels_listall_v2(token)
    save_data()
    return dumps(channels_list)

################################################################################
##                             CHANNEL ROUTES                                 ##
################################################################################

@APP.route('/channel/details/v2', methods=['GET'])
def channel_details():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    channel_details = channel_details_v2(token, channel_id)
    save_data()
    return dumps(channel_details)

@APP.route('/channel/invite/v2', methods=['POST'])
def channel_invite():
    data = request.get_json()
    channel_invite_v2(data['token'], data['channel_id'], data['u_id'])
    save_data()
    return dumps({})

@APP.route('/channel/join/v2', methods=['POST'])
def channel_join():
    data = request.get_json()
    channel_join_v2(data['token'], data['channel_id'])
    save_data()
    return dumps({})

@APP.route('/channel/addowner/v1', methods=['POST'])
def channel_addowner():
    data = request.get.json()
    channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])
    save_data()
    return dumps({})

@APP.route('/channel/messages/v2', methods=['GET'])
def channel_messages():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    channel_messages = channel_messages_v2(token, channel_id, start)
    save_data()
    return dumps(channel_messages)

@APP.route('/channel/leave/v1', methods=['POST'])
def channel_leave():
    data = request.get_json()
    channel_leave_v1(data['token'], data['channel_id'])
    save_data()
    return dumps({})

################################################################################
##                             MESSAGE ROUTES                                 ##
################################################################################

@APP.route('/message/send/v1', methods=['POST'])
def message_send():
    data = request.get_json()
    return dumps(message_send(**data))

@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    clear_v1()
    save_data()
    return dumps({})

def save_data():
    global DATA_STORE
    pickle_data()
    DATA_STORE = get_data()
    with open('datastore.p', 'wb') as FILE:
        pickle.dump(DATA_STORE, FILE)
    return DATA_STORE

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
