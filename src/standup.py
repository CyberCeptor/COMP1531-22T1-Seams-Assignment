"""
Filename: standup.py

Author: Zefan Cao(z5237177)
Created: 03/04/2022 - 14/04/2022

Description: - start the standup
             - check the standup is active
             - send messages
"""
from src.data_store import data_store
from src.error import InputError, AccessError
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_channel_id, check_user_is_member,\
                    check_valid_auth_id
from datetime import datetime, timedelta, timezone
from threading import Timer
from src.message import message_send_v1

def standup_start_v1(token, channel_id, length):
    """
    This function is about the standup process, if messages are attempted to be 
    sent. They will be buffered, then be sent after a length time 
    At the same time they will be added to a message queue.
    Arguments:
        token (str)      - an unique string match a valid user
        channel_id (int) - the unique valid number of a channel
        length (int)     - the length of time for a standup period
                                                  
    Exceptions:
        InputError  - invalid channel id
                    - length is invalid
                    - a standup is currently running
        AccessError - the user is not in the channel
    
    Return Value:
        time_finish(int) - is a timestamp
    """
    store = data_store.get()
    # check valid token
    token_valid_check(token)
    # get user id from token
    user_id = token_get_user_id(token)
    # check valid user id
    check_valid_auth_id(user_id)
    # check valid channel id 
    channel_data = check_valid_channel_id(channel_id)

    # check user is not in channel
    if check_user_is_member(user_id, channel_data, 'all_members') is None:
        raise AccessError('Inviter is not in the channel')

    # check length
    check_length(length)
    
    # get the current time by calling datetime.now
    begin_time = datetime.now()
    # get the end time by calling timedelta with length
    end_time = begin_time + timedelta(seconds = length)

    # check the standup whether running currently or not
    if channel_data['standup']['is_active']:
        raise InputError(
            'An active standup is currently running in this channel'
        )

    # get the finish time, converted it to an UTC timestamp
    # Source: https://www.geeksforgeeks.org/get-utc-timestamp-in-python/
    time_finish = int(end_time.replace(tzinfo=timezone.utc).timestamp())
    
    # add the length, begin_time, end_time into standup
    # coverting begin and end time to an isoformat.
    channel_data['standup']['is_active'] = True
    channel_data['standup']['finish_time'] = end_time.isoformat()
    
    timer = Timer(length, standup_send_collect_messages, [token, channel_data])
    timer.start()

    # Saves data
    data_store.set(store)
    
    # return a dic
    return {'time_finish': time_finish}

def standup_active_v1(token, channel_id):
    '''
    This function is to check the standup whether is active or not
    Arguments:
        token (str)      - an unique string match a valid user
        channel_id (int) - the unique valid number of a channel
                                                  
    Exceptions:
        InputError  - invalid channel id
        AccessError - user is not in the channel
    
    Return Value:
        Returns a dictionary including  is_active and timefinish
    '''
    data_store.get()
    # check valid token
    token_valid_check(token)
    # get user id from token
    user_id = token_get_user_id(token)
    # check valid user id
    check_valid_auth_id(user_id) 
    # check valid channel id
    channel_data = check_valid_channel_id(channel_id)

    # check user is not in channel
    if check_user_is_member(user_id, channel_data, 'all_members') is None:
        raise AccessError(description='Inviter is not in the channel')
    
    value = {} # create an empty dic

    if channel_data['standup']['is_active']:
        finish_time = datetime.fromisoformat(
            channel_data['standup']['finish_time'])

    # Add the is_active into value dic
    value['is_active'] = channel_data['standup']['is_active']

    if value['is_active']:
        value['time_finish'] = int(
            finish_time.replace(tzinfo=timezone.utc).timestamp())
    else:
        value['time_finish'] = None
    return value

def standup_send_v1(token, channel_id, message):
    """
    This function is to send message during the standup period
    
    Arguments:
        token (str)      - an unique string match a valid user
        channel_id (int) - the unique valid number of a channel
        message (str)    - a string of characters
                                                  
    Exceptions:
        InputError  - invalid channel id
                    - length is invalid
                    - a standup is currently running
        AccessError - the user is not in the channel
    
    Return Value: N/A
    """
    data_store.get()
    # check valid token
    token_valid_check(token)
    # get user id from token
    user_id = token_get_user_id(token)
    # check valid user id
    user = check_valid_auth_id(user_id) 
    # check valid channel id
    channel_data = check_valid_channel_id(channel_id)

    if isinstance(message, str) is False:
        raise InputError('wrong type of messages')

    if len(message) > 1000:
        raise InputError('Length of message is over 1000 characters.')
    
    # check user is not in channel
    if check_user_is_member(user_id, channel_data, 'all_members') is None:
        raise AccessError('Inviter is not in the channel')
    
    # check the standup whether running currently or not
    if channel_data['standup']['is_active'] is False:
        raise InputError(
            'An active standup is not currently running in this channel'
        )

    message_name = user['handle']
    collect_messages = f'{message_name}: {message}'
    channel_data['standup']['messages_buffer'].append(collect_messages)

    return {}

def standup_send_collect_messages(token, channel):
    """
    This function is to send message in the buffer
    
    Arguments:
        token (str)      - an unique string match a valid user
        channel (dic)    - a dictionary in channels
                                                  
    Exceptions: N/A

    Return Value: N/A
    """
    if len(channel['standup']['messages_buffer']) > 0:
        packaged_message = '\n'.join(channel['standup']['messages_buffer'])
        message_send_v1(token, channel['channel_id'], packaged_message)

    channel['standup']['is_active'] = False
    channel['standup']['messages_buffer'] = []
    channel['standup']['time_finish'] = None

def check_length(length):
    '''
    This function is to check the length whether is valid
    Arguments:
        length (int)      - time(s)
    
    Exceptions: InputError - invalid length

    Return Value: N/A
    '''
    if type(length) is bool:
        raise InputError('Invalid length')
    
    if isinstance(length, int) is False:
        raise InputError('Invalid length type')
    
    if length < 0:
        raise InputError('Length is invalid')

