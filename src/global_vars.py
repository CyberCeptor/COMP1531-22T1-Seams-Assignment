
"""
File: globals.py

"""

expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZ\
                CI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3OTc3ODgwfQ.366QL\
                XfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'

unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZ\
                CI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPW\
                iR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'


valid_email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

DM_ID_COUNTER = 0
MESSAGE_ID_COUNTER = 0
SESSION_ID_COUNTER = 0

def new_id(option):
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
