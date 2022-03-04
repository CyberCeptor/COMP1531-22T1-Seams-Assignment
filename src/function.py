####### The function.py is written by zefan cao  z5237177
#The function.py is only used in channel_invite_v1 and channel_join_v1 from channel.py
#
#
from src.error import InputError
from src.error import AccessError
from src.data_store import *
from src.channels import *

store = data_store.get()
# Create check_valid_invitee function 
def check_valid_invitee(u_id):
    snumber = False
    for user in store['users']:  #use the value stored in the data_store dictionary
        if u_id == user['id']:
            snumber = True   
    if snumber == False: 
        raise InputError('Inviter is invalid')
    return
    
# Create check_valid_inviter function 
def check_valid_inviter(auth_user_id):
    snumber = False
    for user in store['users']:  #use the value stored in the data_store dictionary
        if auth_user_id == user['id']:
            snumber = True
    if snumber == False: 
        raise InputError('Inviter is invalid')
    return 

# Create a function check the channel is valid or not
def check_valid_channel(channel_id):
    snumber = False
    for channel in store['channels']: #use the value stored in the data_store dictionary
        if channel['channel_id'] == channel_id:
            snumber = True
    if snumber == False:
        raise InputError('Channel is invalid')
    return

# Create a function to test whether the invitee is already in channel
def check_invitee_existin_channel(u_id, channel_id):
    snumber = True
    for channel in store['channels']: #use the value stored in the data_store dictionary
        if channel['channel_id'] == channel_id: #use the value stored in the channel dictionary
            for member in channel['all_members']: #use the value stored in the channel dictionary
                if u_id == member:
                    snumber = False
    if snumber == False:
        raise InputError('Invitee is exist in Channel')
    return

# Create a function to test whether the inviter is not in channel
def check_inviter_existin_channel(auth_user_id, channel_id):  
    snumber = False 
    for channel in store['channels']: #use the value stored in the data_store dictionary
        if channel['channel_id'] == channel_id: #use the value stored in the channel dictionary
            for member in channel['all_members']: #use the value stored in the memeber dictionary
                if auth_user_id == member:
                    snumber = True
    if snumber == False:
        raise AccessError('Inviter is not in Channnel')
    return


#Create a function to add the invitee
def add_invitee(u_id, channel_id):  
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for user in store['users']:
                if u_id == user['id']:
                    channel['all_members'].append(user)
                    
                    return

#Create a function to check the user is a global owner or not 
def check_owner_global(auth_user_id):
    for user in store['users']:
        if user['id'] == auth_user_id:
            tnumber = user['permission_id']
    if tnumber == 1:
        return True
    return False

#Create a function to check the channel is public or not
def check_public_channel(channel_id):
    '''     Failure first
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            snumber = channel['is_public']
        raise InputError('Channel is invalid')
    if snumber == False:
        raise AccessError('Channel is private')
    return
    '''
    # based on examples written by others: https://github.com/eustace65
    if is_public(channel_id) == False :
        raise AccessError('Channel is private') 
    return

#Create the function used in the check_public_channel function
def is_public(channel_id):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel['is_public']
        raise InputError('Channel is invalid')
    