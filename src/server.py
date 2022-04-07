import sys  
import signal
import pickle
from src import config
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.dm import dm_create_v1, dm_list_v1, dm_details_v1, dm_remove_v1,\
                   dm_leave_v1, dm_messages_v1

from src.auth import auth_register_v2, auth_login_v2, auth_logout_v1
from src.user import user_profile_v1, user_profile_setemail_v1, \
                     user_profile_setname_v1, user_profile_sethandle_v1

from src.admin import admin_userpermission_change, admin_user_remove
from src.other import clear_v1
from src.token import token_valid_check, token_get_user_id
from src.users import users_all_v1

from src.channel import channel_details_v2, channel_invite_v2,\
                        channel_addowner_v1, channel_removeowner_v1,\
                        channel_join_v2, channel_messages_v2, channel_leave_v1
from src.message import message_send_v1, message_remove_v1, message_edit_v1,\
                        message_senddm_v1, message_pin_v1

from src.channels import channels_create_v2, channels_list_v2,\
                         channels_listall_v2

from src.data_store_pickle import pickle_data, set_prev_data


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

################################################################################
##                            DATA_STORE PICKLING                             ##
################################################################################

DATA_STORE = {}

def get_data():
    global DATA_STORE
    try:
        DATA_STORE = pickle.load(open('datastore.p', 'rb'))
        set_prev_data(DATA_STORE)
    except Exception:
        pass
    return DATA_STORE

def save_data():
    global DATA_STORE
    pickle_data()
    DATA_STORE = get_data()
    return DATA_STORE

DATA_STORE = get_data()

################################################################################
##                              AUTH ROUTES                                   ##
################################################################################

@APP.route('/auth/register/v2', methods=['POST'])
def register():
    data = request.get_json()
    user = auth_register_v2(data['email'], data['password'],
                            data['name_first'], data['name_last'])
    save_data()
    return dumps(user)

@APP.route('/auth/login/v2', methods=['POST'])
def login():
    data = request.get_json()
    user = auth_login_v2(data['email'], data['password'])
    save_data()
    return dumps(user)

@APP.route('/auth/logout/v1', methods=['POST'])
def logout():
    data = request.get_json()
    auth_logout_v1(data['token'])
    save_data()
    return dumps({})

################################################################################
##                              USERS ROUTES                                  ##
################################################################################

@APP.route('/users/all/v1', methods=['GET'])
def get_all_users():
    token = request.args.get('token')
    users = users_all_v1(token)
    save_data()
    return dumps(users)

################################################################################
##                              USER ROUTES                                   ##
################################################################################

@APP.route('/user/profile/v1', methods=['GET'])
def user_profile():
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    profile = user_profile_v1(token, u_id)
    save_data()
    return jsonify(profile)

@APP.route('/user/profile/setemail/v1', methods=['PUT'])
def user_setemail():
    email_data = request.get_json()
    token = email_data['token']
    email = email_data['email']
    user_profile_setemail_v1(token, email)
    save_data()
    return dumps({})

@APP.route('/user/profile/setname/v1', methods=['PUT'])
def user_setname():
    name_data = request.get_json()
    token = name_data['token']
    name_first = name_data['name_first']
    name_last = name_data['name_last']
    user_profile_setname_v1(token, name_first, name_last)
    save_data()
    return dumps({})

@APP.route('/user/profile/sethandle/v1', methods=['PUT'])
def user_sethandle():
    handle_data = request.get_json()
    token = handle_data['token']
    handle_str = handle_data['handle_str']
    user_profile_sethandle_v1(token, handle_str)
    save_data()
    return dumps({})

################################################################################
##                              ADMIN ROUTES                                  ##
################################################################################

@APP.route('/admin/userpermission/change/v1', methods=['POST'])
def change_perms():
    data = request.get_json()
    admin_userpermission_change(data['token'], data['u_id'], 
                                data['permission_id'])
    save_data()
    return dumps({})

@APP.route('/admin/user/remove/v1', methods=['DELETE'])
def remove_user():
    data = request.get_json()
    admin_user_remove(data['token'], data['u_id'])
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
    data = request.get_json()
    channel_addowner_v1(data['token'], data['channel_id'], data['u_id'])
    save_data()
    return dumps({})

@APP.route('/channel/removeowner/v1', methods=['POST'])
def channel_removeowner():
    data = request.get_json()
    channel_removeowner_v1(data['token'], data['channel_id'], data['u_id'])
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
    token_valid_check(data['token'])
    user_id = token_get_user_id(data['token'])
    channel_leave_v1(user_id, data['channel_id'])
    save_data()
    return dumps({})

################################################################################
##                             MESSAGE ROUTES                                 ##
################################################################################

@APP.route('/message/send/v1', methods=['POST'])
def message_send():
    data = request.get_json()
    msg_id = message_send_v1(data['token'], data['channel_id'], data['message'])
    save_data()
    return dumps(msg_id)

@APP.route('/message/edit/v1', methods=['PUT'])
def message_edit():
    data = request.get_json()
    message_edit_v1(data['token'], data['message_id'], data['message'])
    save_data()
    return dumps({})

@APP.route('/message/remove/v1', methods=['DELETE'])
def message_remove():
    data = request.get_json()
    message_remove_v1(data['token'], data['message_id'])
    save_data()
    return dumps({})

@APP.route('/message/senddm/v1', methods=['POST'])
def message_senddm():
    data = request.get_json()
    msg_id = message_senddm_v1(data['token'], data['dm_id'], data['message'])
    save_data()
    return dumps(msg_id)

@APP.route('/message/pin/v1', methods=['POST'])
def message_pin():
    data = request.get_json()
    message_pin_v1(data['token'], data['message_id'])
    save_data()
    return dumps({})

################################################################################
##                             DM ROUTES                                      ##
################################################################################

@APP.route('/dm/create/v1', methods=['POST'])
def dm_create_server():
    store = request.get_json()
    token = store['token']
    u_ids = store['u_ids']
    dm = dm_create_v1(token, u_ids)
    save_data()
    return dumps(dm)

@APP.route('/dm/list/v1', methods=['GET'])
def dm_list_server():
    token = request.args.get('token')
    dms_list = dm_list_v1(token)
    save_data()
    return dumps(dms_list)

@APP.route('/dm/details/v1', methods=['GET'])
def dm_details_server():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    dm_details = dm_details_v1(token,dm_id)
    save_data()
    return dumps(dm_details)

@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove_server():
    store = request.get_json()
    token = store['token']
    dm_id = store['dm_id']
    dm_remove_v1(token,dm_id)
    save_data()
    return dumps({})

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    store = request.get_json()
    dm_id = store['dm_id']
    token_valid_check(store['token'])
    auth_id = token_get_user_id(store['token'])
    dm_leave_v1(auth_id, dm_id)
    save_data()
    return dumps({})

@APP.route('/dm/messages/v1', methods=['GET'])
def dm_messages():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')
    dm_messages = dm_messages_v1(token, dm_id, start)
    save_data()
    return dumps(dm_messages)

################################################################################
##                               CLEAR ROUTE                                  ##
################################################################################

@APP.route('/clear/v1', methods=['DELETE'])
def clear():
    clear_v1()
    save_data()
    return dumps({})

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
