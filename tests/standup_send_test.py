"""
Filename: standup_send_test.py

Author: Zefan Cao(z5237177)
Created: 03/04/2022 - 14/04/2022

Description: pytest for standup_send
"""
import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1
from src.standup import standup_start_v1, standup_send_v1
from datetime import datetime, timezone


def test_standup_send_valid():
    """
    clears any data stored in data_store and registers users with the
    given information, test send valid
    """
    # Clear data
    clear_v1()
    
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'Channel1', False)
    channel_id = channel['channel_id']
    
    # start a standup
    standup_start_v1(token, channel_id, 1)
    return_value1 = standup_send_v1(token, channel_id, 'Hello World')
    
    assert isinstance(return_value1, dict)    
    assert return_value1 == {}

def test_standup_send_invalid_channel():
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
        standup_send_v1(token, 44, 'Hello World')

    with pytest.raises(InputError): 
        standup_send_v1(token, -44, 'Hello World')

    with pytest.raises(InputError): 
        standup_send_v1(token, '', 'Hello World')

    with pytest.raises(InputError): 
        standup_send_v1(token, 'ste', 'Hello World')
    
    with pytest.raises(InputError): 
        standup_send_v1(token, False, 'Hello World')

def test_standup_send_valid_length():
    """
    clears any data stored in data_store and registers users with the
    given information, test length is over 1000 characters
    """
    # Clear data
    clear_v1()
    
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'Channel1', True)
    channel_id = channel['channel_id']
    standup_start_v1(token, channel_id, 1)
    # create a message is over 1000 characters
    message = 'hello' * 201

    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, message)

def test_standup_send_inactive():
    """
    clears any data stored in data_store and registers users with the
    given information, test standup is not currently running
    """
    # Clear data
    clear_v1()
    
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'Channel1', False)
    channel_id = channel['channel_id']

    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, 'message')

def test_standup_send_is_not_in_channel():
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

    standup_start_v1(token, channel_id, 1)
    
    with pytest.raises(AccessError):
        standup_send_v1(token2, channel_id, 'hello world')

def test_standup_send_invalid_message():
    """
    clears any data stored in data_store and registers users with the
    given information, test invalid message
    """
    # Clear data
    clear_v1()
    
    user1 = auth_register_v2('wky@gmail.com', '346758', 'wang', 'kaiyan')
    token = user1['token']
    channel = channels_create_v2(token, 'Channel1', True)
    channel_id = channel['channel_id']
    standup_start_v1(token, channel_id, 1)

    with pytest.raises(InputError):
        standup_send_v1(token, channel_id, 4)