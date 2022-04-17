import sys  
import signal
import pickle
from src import config
from json import dumps
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_mail import Mail, Message

from src.dm import dm_create_v1, dm_list_v1, dm_details_v1, dm_remove_v1,\
                   dm_messages_v1

from src.auth import auth_register_v2, auth_login_v2, generate_reset_code, \
                     passwordreset_reset_v1
from src.user import user_profile_v1, user_profile_setemail_v1, \
                     user_profile_setname_v1, user_profile_sethandle_v1, \
                     user_profile_uploadphoto_v1, user_stats_v1

from src.admin import admin_userpermission_change, admin_user_remove
from src.other import clear_v1
from src.token import token_remove
from src.users import users_all_v1, users_stats_v1

from src.search import search_v1

from src.channel import channel_details_v2, channel_invite_v2,\
                        channel_addowner_v1, channel_removeowner_v1,\
                        channel_join_v2, channel_messages_v2
from src.message import message_send_v1, message_remove_v1, message_edit_v1,\
                        message_senddm_v1, message_pin_v1, message_react_v1, \
                        message_unreact_v1, message_unpin_v1, message_share_v1,\
                        message_sendlater_v1, message_sendlaterdm_v1
                        
from src.channels import channels_create_v2, channels_list_v2,\
                         channels_listall_v2

from src.notifications import notifications_get_v1

from src.data_store_pickle import pickle_data, set_prev_data

from src.standup import standup_start_v1, standup_active_v1,\
                        standup_send_v1

from src.channel_dm_helpers import leave_channel_dm

from src.error import InputError

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
##                                MAIL CONFIG                                 ##
################################################################################

# following https://pythonbasics.org/flask-mail/

mail = Mail(APP)

EMAIL = 'donotreply.pwreset@gmail.com'

APP.config['MAIL_SERVER'] = 'smtp.gmail.com'
APP.config['MAIL_PORT'] = 465
APP.config['MAIL_USERNAME'] = EMAIL
APP.config['MAIL_PASSWORD'] = 'P@ssword1531'
APP.config['MAIL_USE_TLS'] = False
APP.config['MAIL_USE_SSL'] = True

mail = Mail(APP)

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
        pickle_data()
    return DATA_STORE

def save_data():
    global DATA_STORE
    pickle_data()
    DATA_STORE = get_data()

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
    token_remove(data['token'])
    save_data()
    return dumps({})

@APP.route('/auth/passwordreset/request/v1', methods=['POST'])
def request_pwreset():
    data = request.get_json()
    code = generate_reset_code(data['email'])
    if code is not None:
        # following https://pythonbasics.org/flask-mail/
        msg = Message('Seams Password Reset', sender = EMAIL,
                      recipients = [data['email']])
        msg.body = f'Your reset code is: {code}'
        mail.send(msg)
    save_data()
    return dumps({})

@APP.route('/auth/passwordreset/reset/v1', methods=['POST'])
def pw_reset():
    data = request.get_json()
    passwordreset_reset_v1(data['reset_code'], data['new_password'])
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

@APP.route('/users/stats/v1', methods=['GET'])
def get_users_stats():
    global DATA_STORE
    token = request.args.get('token')
    stats = users_stats_v1(token)
    save_data()
    return dumps(stats)

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

@APP.route('/user/profile/uploadphoto/v1', methods=['POST'])
def user_uploadphoto():
    data = request.get_json()
    token = data['token']
    url = data['img_url']
    x_start = data['x_start']
    x_end = data['x_end']
    y_start = data['y_start']
    y_end = data['y_end']
    user_profile_uploadphoto_v1(token, url, x_start, y_start, x_end, y_end)
    save_data()
    return dumps({})


@APP.route('/static/<user_id>.jpg', methods=['GET'])
def user_profile_image(user_id):
    """A Route to store the profile picture"""
    try:
        send_file(f'static/{user_id}.jpg', mimetype='image/jpeg')
        print("File exists.")
    except:
        raise InputError("File does not exist") from InputError
    # https://flask.palletsprojects.com/en/2.1.x/api/
    return send_file(f'static/{user_id}.jpg', mimetype='image/jpeg')

@APP.route('/user/stats/v1', methods=['GET'])
def get_user_stats():
    global DATA_STORE
    token_data = request.args.get('token')
    stats = user_stats_v1(token_data)
    save_data()
    return dumps(stats)


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
    leave_channel_dm(data['token'], None, data['channel_id'], 'channel')
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

@APP.route('/message/senddm/v1', methods=['POST'])
def message_senddm():
    data = request.get_json()
    msg_id = message_senddm_v1(data['token'], data['dm_id'], data['message'])
    save_data()
    return dumps(msg_id)

@APP.route('/message/sendlater/v1', methods=['POST'])
def message_sendlater():
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    time_sent = data['time_sent']
    msg_id = message_sendlater_v1(token, channel_id, message, time_sent)
    save_data()
    return dumps(msg_id)

@APP.route('/message/sendlaterdm/v1', methods=['POST'])
def message_sendlaterdm():
    data = request.get_json()
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']
    time_sent = data['time_sent']
    msg_id = message_sendlaterdm_v1(token, dm_id, message, time_sent)
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

@APP.route('/message/pin/v1', methods=['POST'])
def message_pin():
    data = request.get_json()
    message_pin_v1(data['token'], data['message_id'])
    save_data()
    return dumps({})

@APP.route('/message/unpin/v1', methods=['POST'])
def message_unpin():
    data = request.get_json()
    message_unpin_v1(data['token'], data['message_id'])
    save_data()
    return dumps({})

@APP.route('/search/v1', methods=['GET'])
def search():
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    message_return = search_v1(token, query_str)
    save_data()
    return dumps(message_return)
    
@APP.route('/message/react/v1', methods=['POST'])
def message_react():
    data = request.get_json()
    message_react_v1(data['token'], data['message_id'], data['react_id'])
    save_data()
    return dumps({})

@APP.route('/message/unreact/v1', methods=['POST'])
def message_unreact():
    data = request.get_json()
    message_unreact_v1(data['token'], data['message_id'], data['react_id'])
    save_data()
    return dumps({})

@APP.route('/message/share/v1', methods=['POST'])
def message_share():
    data = request.get_json()
    token = data['token']
    og_message_id = data['og_message_id']
    message = data['message']
    channel_id = data['channel_id']
    dm_id = data['dm_id']
    msg_id = message_share_v1(token, og_message_id, message, channel_id, dm_id)
    save_data()
    return dumps(msg_id)

################################################################################
##                             DM ROUTES                                      ##
################################################################################

@APP.route('/dm/create/v1', methods=['POST'])
def dm_create():
    data = request.get_json()
    dm = dm_create_v1(data['token'], data['u_ids'])
    save_data()
    return dumps(dm)

@APP.route('/dm/list/v1', methods=['GET'])
def dm_list():
    token = request.args.get('token')
    dms_list = dm_list_v1(token)
    save_data()
    return dumps(dms_list)

@APP.route('/dm/details/v1', methods=['GET'])
def dm_details():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    dm_details = dm_details_v1(token, dm_id)
    save_data()
    return dumps(dm_details)

@APP.route('/dm/remove/v1', methods=['DELETE'])
def dm_remove():
    data = request.get_json()
    dm_remove_v1(data['token'], data['dm_id'])
    save_data()
    return dumps({})

@APP.route('/dm/leave/v1', methods=['POST'])
def dm_leave():
    data = request.get_json()
    leave_channel_dm(data['token'], None, data['dm_id'], 'dm')
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
##                             STANDUP ROUTES                                 ##
################################################################################

@APP.route('/standup/start/v1', methods=['POST'])
def standup_start():
    store = request.get_json()
    time_finish = standup_start_v1(
        store['token'], store['channel_id'], store['length']
    )
    save_data()
    return dumps(time_finish)

@APP.route('/standup/active/v1', methods = ['GET'])
def standup_active():
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    standup_info = standup_active_v1(token, channel_id)
    save_data()
    return dumps(standup_info)

@APP.route('/standup/send/v1', methods=['POST'])
def standup_send():
    store = request.get_json()
    standup_send_v1(store['token'], store['channel_id'], store['message'])
    save_data()
    return dumps({})

################################################################################
##                            NOTIFICATIONS ROUTE                             ##
################################################################################

@APP.route('/notifications/get/v1', methods=['GET'])
def get_notifs():
    token = request.args.get('token')
    notifs = notifications_get_v1(token)
    save_data()
    return dumps(notifs)

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
