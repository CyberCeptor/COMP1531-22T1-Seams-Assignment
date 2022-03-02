import pytest
from src.auth import auth_register_v1
from src.other import clear_v1
from src.error import InputError
from src.error import AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.channel import channel_invite_v1
from src.data_store import data_store
from src.channel import channel_join_v1


### Test Chanel_invite    Zefan Cao(Van)
#
#
#
# Test successs
def test_invite_successful():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    createchannel =channels_create_v1(inviter_info['auth_user_id'], 'namechannelwky', True)  # The channel id will be 0
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    channel_invite_v1(inviter_info['auth_user_id'], createchannel['channel_id'], invitee_info['auth_user_id'])
    now_channle = data_store['channels']
    now_channel_name = now_channle[0]
    now_member = now_channel_name['members']
    assert len(now_member) == 2

# Inputerror:Test the function has an invalid channel_id
def test_invite_wrong_channel():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    '''createchannel =channels_create_v1(inviter_info['auth_user_id'], 'namechannelwky', True) # The channel id will be 0'''
    with pytest.raises(InputError):
        channel_invite_v1(inviter_info['auth_user_id'], 0, invitee_info['auth_user_id'])

# Inputerror:Test the function has an invalid user.
def test_invite_wrong_invitee():
    clear_v1()
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    with pytest.raises(InputError):
        channel_invite_v1(1, 0, invitee_info['auth_user_id'])

# Inputerror:Test the invitee is already in channel
def test_channel_invite_user_already_joined():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    channels_create_v1(inviter_info['auth_user_id'], 'namewkychannel', True)
    channel_join_v1(invitee_info['auth_user_id'], 0)
    with pytest.raises(InputError):
        channel_invite_v1(1, 0, invitee_info['auth_user_id'],)

# Accesserror: Test the inviter is not in the channel
def test_channel_invite_unauthorised():
    clear_v1()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    createchannel =channels_create_v1(inviter_info['auth_user_id'], 'namechannelwky', True)
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    truowner_info = auth_register_v1('limingzhe@gmail.com', 'lmz19991123', 'Li', 'mingzhe')
    with pytest.raises(AccessError):
        channel_invite_v1(truowner_info['auth_user_id'], createchannel['channel_id'], invitee_info['auth_user_id'])


