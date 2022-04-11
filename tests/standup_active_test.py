"""
Filename: standup_active_test.py

Author: Zefan Cao(z5237177)
Created: 03/04/2022 - 14/04/2022

Description: pytest for standup_active
"""
import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.standup import standup_active_v1, standup_start_v1
from datetime import datetime, timezone

def test_standup_active_valid():
    """
    clears any data stored in data_store and registers users with the
    given information, test standup active valid
    """
    # Clear data
    clear_v1() 
    
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token'] 
    channel = channels_create_v2(token, 'Channel1', False) 
    channel_id = channel['channel_id']

    stand = standup_active_v1(token, channel_id)
    assert (isinstance(stand, dict) == True)
    assert stand['is_active'] == False
    assert stand['time_finish'] == None

    standup_start_v1(token, channel_id, 1)
    stand1 = standup_active_v1(token, channel_id)
    assert (isinstance(stand1, dict) == True)
    assert stand1['is_active'] == True
    assert (isinstance(stand1['time_finish'], int) == True)

def test_standup_active_invalid_channel():
    """
    clears any data stored in data_store and registers users with the
    given information, test invalid channel
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channels_create_v2(token, 'Channeld', True)
    with pytest.raises(InputError):
        standup_start_v1(token, 44, 1)
    
    with pytest.raises(InputError):
        standup_start_v1(token, -44, 1)
    
    with pytest.raises(InputError):
        standup_start_v1(token, '', 1)
    
    with pytest.raises(InputError):
        standup_start_v1(token, False, 1)
    
    with pytest.raises(InputError):
        standup_start_v1(token, 'DFJK', 1)

def test_standup_active_is_not_in_channel():
    """
    clears any data stored in data_store and registers users with the
    given information, test user is not in channel
    """
    # Clear data
    clear_v1()

    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token'] 
    channel = channels_create_v2(token, 'abc', True) 
    channel_id = channel['channel_id']

    user2 = auth_register_v2('lmz@gmail.com', '364832', 'li', 'mingzhe')
    token2 = user2['token'] 

    with pytest.raises(AccessError):
        standup_active_v1(token2, channel_id)