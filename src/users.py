"""
Filename: users.py

Author: Aleesha Bunrith(z5371516), Jenson Morgan(z5360181)
Created: 21/03/2022 - 30/03/2022
       : 15/04/2022 - 17/04/2022

Description: Implementation for getting the info of all current users
"""

from src.token import token_valid_check

from src.data_store import data_store

import time


@token_valid_check
def users_all_v1(token):
    """
    returns the data of every user in the stored data, excluding those who have
    been removed

    Arguments:
        token (str) - a valid jwt token string

    Exceptions: N/A

    Return Value:
        Returns a dict containing each users' u_id, email, name_first,
        name_last, and handle_str if the user has not been removed
    """

    store = data_store.get()

    return {
        'users': [{
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['first'],
            'name_last': user['last'],
            'handle_str': user['handle'],
        } for user in store['users'] if user['removed'] is False]
    }


@token_valid_check
def users_stats_v1(token):
    """
    Generates the statistic's from the use of UNSW Seams.
    Calculates the number of channels/DM's/messages that exist, 
    and the utilization rate. 
        (num_users_who_have_joined_at_least_one_channel_or_dm / num_users)

    Arguments: 
        - token: the user requesting the statistics
    
    Exceptions:
        - N/A

    Return Value:
        - 'workspace_stats': A dictionary containing the statistics
    """

    store = data_store.get()
    users_list = []
    time_stamp = int(time.time())
    channels_total = len(store['channels'])
    dms_total = len(store['dms'])
    messages_total = 0

    '''Calculate the number of messages in all channels'''
    for channels in store['channels']:
        messages_total += len(channels['messages'])
    
    '''Calculate the number of messages in all DM's'''
    for dms in store['dms']:
        messages_total += len(dms['messages'])

    '''get the total number of users of SEAMS'''
    users_total = len(store['users'])

    '''Add all Channel users user_id to the users list.'''
    for channels in store['channels']:
        for members in channels['all_members']:
            users_list.append(members['u_id'])

    '''Add all DM users user_id to the users list
    Checks if the user is not already in the list from the channels'''
    for dms in store['dms']:
        for members in dms['members']:
            if members['u_id'] not in users_list:
                users_list.append(members['u_id'])

    '''Create the channels_exist, dms_exist, messages_exist dictionaries.'''
    channels_exist = {
        'num_channels_exist': channels_total,
        'time_stamp': time_stamp
    }
    dms_exist = {
        'num_dms_exist': dms_total,
        'time_stamp': time_stamp,
    }
    messages_exist = {
        'num_messages_exist': messages_total,
        'time_stamp': time_stamp
    }

    '''num_users_who_have_joined_at_least_one_channel_or_dm / num_users'''
    util_rate = round(len(users_list) / users_total, 1)

    '''Append the statistics to the workspace_stats'''
    store['workspace_stats']['channels_exist'].append(channels_exist)
    store['workspace_stats']['dms_exist'].append(dms_exist)
    store['workspace_stats']['messages_exist'].append(messages_exist)
    store['workspace_stats']['utilization_rate'] = util_rate

    data_store.set(store)
    
    return {
        'workspace_stats': store['workspace_stats']
    }