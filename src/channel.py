from src.error import InputError
from src.error import AccessError
from src.data_store import *
from src.function import *
from src.channels import *

def channel_invite_v1(auth_user_id, channel_id, u_id):
    check_valid_inviter(auth_user_id) # check the inviter is valid or not
    check_valid_invitee(u_id)# check the invitee is valid or not
    check_valid_channel(channel_id) # check the channel is valid or not
    check_invitee_existin_channel(u_id,channel_id) #check the invitee whether is already in the channnel
    check_inviter_existin_channel(auth_user_id,channel_id) #check the inviter is not in the channel
    add_invitee(u_id, channel_id) #add user
    
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'email': 'example@gmail.com',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'haydenjacobs',
            }
        ],
    }

def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }
#### channel_join_v1 is written by zefan cao z5237177
#
#
#
def channel_join_v1(auth_user_id, channel_id):
    check_valid_channel(channel_id)   #check the channle is valid or not
    check_valid_invitee(auth_user_id) #check the invitee is valid or not
    check_invitee_existin_channel(auth_user_id,channel_id)  #check the invitee whether is already in the channel
    if check_owner_global(auth_user_id) == True: #check the user whether is a global owner (if the user is a global owner, add immediately, even this is a priavate channel)
        add_invitee(auth_user_id, channel_id) # add user
        return 
    check_public_channel(channel_id) #check the channel whether is public
    add_invitee(auth_user_id, channel_id) #add user
    return {
    }

