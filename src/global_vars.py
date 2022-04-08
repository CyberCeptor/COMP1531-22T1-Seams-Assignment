""""
Filename: global_vars.py

Author: group
Created: 24/02/2022 - 27/03/2022

Description: global variables and functions used across files
"""

import jwt

key = 'hotpot'
algorithm = 'HS256'

# an expired, unsaved token
expired_token = jwt.encode({'id': 44, 'session_id': 200, 'handle': 'firstlast',
                            'exp': 1448474355}, key, algorithm=algorithm)

# an unexpired, unsaved token
unsaved_token = jwt.encode({'id': 44, 'session_id': 200, 'handle': 'firstlast',
                            'exp': 2548474355}, key, algorithm=algorithm)

status_ok = 200
status_input_err = 400
status_access_err = 403

DM_ID_COUNTER = 0
MESSAGE_ID_COUNTER = 0
SESSION_ID_COUNTER = 0

def new_id(option):
    """
    generates a new id for the specified option

    Arguments:
        option (str) - a string denoting which new id we want to generate

    Exceptions: N/A

    Return Value:
        Returns an int that has incremented the last new_id generated by 1
    """

    if option == 'message':
        global MESSAGE_ID_COUNTER
        MESSAGE_ID_COUNTER += 1
        return MESSAGE_ID_COUNTER 
    elif option == 'dm':
        global DM_ID_COUNTER 
        DM_ID_COUNTER += 1
        return DM_ID_COUNTER
    elif option == 'session':
        global SESSION_ID_COUNTER 
        SESSION_ID_COUNTER += 1
        return SESSION_ID_COUNTER
    
def reset_id(option):
    """
    resets the ids for the specified option

    Arguments:
        option (str) - a string denoting which id we want to reset

    Exceptions: N/A

    Return Value:
        Resets the id to 0 and returns
    """
    if option == 'message':
        global MESSAGE_ID_COUNTER
        MESSAGE_ID_COUNTER = 0
        return MESSAGE_ID_COUNTER 
    elif option == 'dm':
        global DM_ID_COUNTER 
        DM_ID_COUNTER = 0
        return DM_ID_COUNTER
    elif option == 'session':
        global SESSION_ID_COUNTER 
        SESSION_ID_COUNTER = 0
        return SESSION_ID_COUNTER
