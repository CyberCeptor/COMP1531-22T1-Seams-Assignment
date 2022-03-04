from src.error import InputError
<<<<<<< HEAD
from src.error import AccessError
from src.data_store import *
from src.function import *
from src.channels import *
=======
from src.other import check_valid_auth_id
from src.other import check_user_is_member
from src.other import check_valid_channel_id

from src.data_store import data_store
>>>>>>> master

def channel_invite_v1(auth_user_id, channel_id, u_id):
    check_valid_inviter(auth_user_id) # check the inviter is valid or not
    check_valid_invitee(u_id)# check the invitee is valid or not
    check_valid_channel(channel_id) # check the channel is valid or not
    check_invitee_existin_channel(u_id,channel_id) #check the invitee whether is already in the channnel
    check_inviter_existin_channel(auth_user_id,channel_id) #check the inviter is not in the channel
    add_invitee(u_id, channel_id) #add user
    
    return {
    }





#  Given a channel with ID channel_id that the authorised user is a member of
#  provide basic details about the channel.
def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    # see if given auth_user_id and channel_id are valid
    check_valid_auth_id(auth_user_id)
    check_valid_channel_id(channel_id)

    is_member = check_user_is_member(auth_user_id, channel_id)
    if is_member == False:
        raise InputError('User does not exist in channel')

    channel = store['channels'][channel_id - 1]

    return {
        'name': channel['name'],
        'is_public': channel['is_public'],
        'owner_members': channel['owner_members'],
        'all_members': channel['all_members'],
    }

# return { name, is_public, owner_members, all_members }


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

