"""
Filename: standup_start_test.py

Author: Zefan Cao(z5237177)
Created: 03/04/2022 - 14/04/2022

Description: pytest for standup_start
"""
import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2#channels_list_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.standup import standup_start_v1#standup_active_v1
from datetime import datetime, timezone

def test_standup_start_valid():
    """
    clears any data stored in data_store and registers users with the
    given information, test standup valid
    """
    # Clear data 
    clear_v1() 
    
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'Channel_1', True)
    channel_id = channel['channel_id']
    
    # calling standup start
    time = standup_start_v1(token, channel_id, 5)
    assert (isinstance(time, dict) == True)
    time_finish = time['time_finish']
    assert (isinstance(time_finish, int) == True)

    # the current time is less than time finish
    now = datetime.now()
    now_timestamp = int(now.replace(tzinfo=timezone.utc).timestamp())
    assert (time_finish > now_timestamp)

def test_standup_start_invalid_channel():
    """
    clears any data stored in data_store and registers users with the
    given information, test invalid channel
    """
    # Clear data
    clear_v1()

    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']

    # test invalid channel
    with pytest.raises(InputError): 
        standup_start_v1(token, 44, 1)

    with pytest.raises(InputError): 
        standup_start_v1(token, -44, 1)

    with pytest.raises(InputError): 
        standup_start_v1(token, '', 1)

    with pytest.raises(InputError): 
        standup_start_v1(token, 'ste', 1)
    
    with pytest.raises(InputError): 
        standup_start_v1(token, False, 1)

def test_standup_start_invalid_length():
    """
    clears any data stored in data_store and registers users with the
    given information, test invalid length
    """
    # Clear data
    clear_v1()

    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'Channel_1', True)

    # test invalid channel
    with pytest.raises(InputError): 
        standup_start_v1(token, channel['channel_id'], None)

    with pytest.raises(InputError): 
        standup_start_v1(token, channel['channel_id'], -55)

    with pytest.raises(InputError): 
        standup_start_v1(token, channel['channel_id'], False)

    with pytest.raises(InputError): 
        standup_start_v1(token, channel['channel_id'], '')
    
    with pytest.raises(InputError): 
        standup_start_v1(token, channel['channel_id'], 'shjdsk')
    
    with pytest.raises(InputError): 
        standup_start_v1(token, channel['channel_id'], [21])

def test_standup_start_standup_repeating():
    """
    clears any data stored in data_store and registers users with the
    given information, test a standuo is running currently
    """
    # Clear data
    clear_v1()

    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'abc', False) 
    channel_id = channel['channel_id']
    standup_start_v1(token, channel_id, 100)
    with pytest.raises(InputError):
        standup_start_v1(token, channel_id, 1)

def test_standup_start_is_not_in_channel():
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
        standup_start_v1(token2, channel_id, 1)