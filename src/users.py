"""
Filename: users.py

Author: Aleesha Bunrith(z5371516)
Created: 21/03/2022 - 30/03/2022

Description: Implementation for getting the info of all current users
"""

from src.token import token_valid_check

from src.data_store import data_store

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
    Fetches the required statistic about the use of UNSW Seams
    Gets all the relevant information of the use of SEAMS by everyone. 
    Dictionary contains: (workspace_stats)
        channels_exist: [{nums_channels_exist, time_stamp}],
        dms_exist: [{nums_dms_exist, time_stamp}],
        messages_exist: [{num_messages_exist, time_stamp}],
        utilization_rate, (num_users_who_have_joined_at_least_one_channel_or_dm / num_users)

    Get the length of:
        store['channels']
        store['dms']
        store['message_count']
    Get a time stamp
    Total number of users in all channels
    Total number of users in all DM's
    Create the workspace_stats dict and append the information found,
    and calculate the utilization_rate. 
    """



    return {}#workspace_stats # dict