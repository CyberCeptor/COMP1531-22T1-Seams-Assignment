"""
File: globals.py

"""

expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZ\
                CI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoxNTQ3OTc3ODgwfQ.366QL\
                XfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'

unsaved_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZ\
                CI6MSwiaGFuZGxlIjoiZmlyc3RsYXN0IiwiZXhwIjoyNTQ3OTc3ODgwfQ.ckPPW\
                iR-m6x0IRqpQtKmJgNLiD8eAEiTv2i8ToK3mkY'

MESSAGE_ID_COUNTER = 0
def new_message_id():
    global MESSAGE_ID_COUNTER 
    MESSAGE_ID_COUNTER  += 1
    return MESSAGE_ID_COUNTER 