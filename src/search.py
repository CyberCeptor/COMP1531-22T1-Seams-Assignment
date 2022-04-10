"""
Filename: search.py

Author: Yangjun Yue(z5317840)
Created: 07/03/2022 - 07/04/2022

Description: implementation for
    - searching for messages containing a given query_string
"""

from src.error import InputError, AccessError
from src.other import check_valid_auth_id, check_user_is_member
from src.token import token_valid_check, token_get_user_id

from src.data_store import data_store

@token_valid_check
def search_v1(token, query_str):
    """
    If token given is authorised user, return a collection of messages
    in all of the channels/DMs that the user has joined that contain 
    the query (case-insensitive). There is no expected order for these messages.

    Arguments:
        token (str)          - unique str representation of user
       query_str (str)       - str that searches for matching messages

    Exceptions:
        InputError  - length of query_str is less than 1 or over 1000 characters
    """
    
    # getting information from date_store
    store = data_store.get()
    
    user_id = token_get_user_id(token)
    check_valid_auth_id(user_id)

    # checking query string input
    if query_str == '':
        raise InputError(description='Empty query string input')

    if len(query_str) > 1000:
        raise InputError(description='Message must not exceed 1000 characters')
    
    # create a list to store all correlated messages and return in the end
    message_return = []
    for channel in store['channels']:
        for message_data in channel['messages']:
            # change everything in lower case,account case insensitivity
            if (query_str.lower() in message_data['message'].lower() and 
                check_user_is_member(user_id, channel, 'all_members')):
                message_return.append(message_data)

    # checking dm case                
    for dm in store['dms']:
        for message_data in dm['messages']:
            # change everything in lower case, account case insensitivity
            if (query_str.lower() in message_data['message'].lower() and 
                check_user_is_member(user_id, dm, 'members')):
                message_return.append(message_data)

    return message_return
