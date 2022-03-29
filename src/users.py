"""
Filename: users.py

Author: Aleesha Bunrith(z5371516)
Created: 21/03/2022 - 30/03/2022

Description: Implementation for getting the info of all current users
"""

from src.token import token_valid_check

from src.data_store import data_store

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
    token_valid_check(token)

    return {
        'users': [{
            'u_id': user['id'],
            'email': user['email'],
            'name_first': user['first'],
            'name_last': user['last'],
            'handle_str': user['handle'],
        } for user in store['users'] if user['removed'] is False]
    }