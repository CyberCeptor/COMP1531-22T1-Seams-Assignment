from ast import Store
import pytest

from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.data_store import *
from src.channel import channel_join_v1


### Test Chanel_invite    Zefan Cao(Van)
#
#
#
# Test successs

def test_invite_successful():
    clear_v1()
    store = data_store.get()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    createchannel =channels_create_v1(inviter_info['auth_user_id'], 'namechannelwky', True)
    
    channel_invite_v1(inviter_info['auth_user_id'], createchannel['channel_id'], invitee_info['auth_user_id'])
    assert len(store['channels'][0]['all_members']) == 2

# Inputerror:Test the function has an invalid channel_id
def test_invite_wrong_channel():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_invite_v1(inviter_info['auth_user_id'], 6, invitee_info['auth_user_id'])

# Inputerror:Test the function has an invalid invitee.
def test_invite_wrong_invitee():
    clear_v1()
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_invite_v1(1, 0, invitee_info['auth_user_id'])

# Inputerror:Test the function has an invalid inviter.
def test_invite_wrong_inviter():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    with pytest.raises(InputError):
        channel_invite_v1(inviter_info['auth_user_id'], 0, 1)

# Inputerror:Test the invitee is already in channel
def test_channel_invite_user_already_joined():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    channels_create_v1(inviter_info['auth_user_id'], 'namewkychannel', True)
    with pytest.raises(InputError):
        channel_invite_v1(inviter_info['auth_user_id'], 0, invitee_info['auth_user_id'],)

# Accesserror: Test the inviter is not in the channel
def test_channel_invite_unauthorised():
    clear_v1()
    truowner_info = auth_register_v1('limingzhe@gmail.com', 'lmz19991123', 'Li', 'mingzhe')
    createchannel =channels_create_v1(truowner_info['auth_user_id'], 'namechatnnelwky', True)  
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    with pytest.raises(AccessError):
        channel_invite_v1(inviter_info['auth_user_id'], createchannel['channel_id'], invitee_info['auth_user_id'])

######## Test channel_join_v1
#
#
#
# Test successful
'''
def test_channel_join_successful():
    clear_v1()
    store = data_store.get()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    newchannel = channels_create_v1(inviter_info['auth_user_id'], 'namechannelwky', True)
    channel_join_v1(invitee_info['auth_user_id'], newchannel['channel_id'])
    assert len(store['channels'][0]['all_members']) == 2
'''
'''
#
def test_channel_join_flockr_owner_joins_private_channel():
    clear_v1()
    userA = auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    userB = auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    newchannel = channels_create(userB['token'], 'validchannelname', False)
    channel.channel_join(userA['token'], newchannel['channel_id'])
    assert len(data['channels'][0]['members']) == 2
'''

# InputError: Channel ID is not a valid channel
def test_channel_join_invalid_channel():
    clear_v1()
    userB = auth_register_v1('validemail2@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    with pytest.raises(InputError):
        channel_join_v1(userB['auth_user_id'], 0)




