def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    '''
Parameters: 
    {auth_user_id,  (int)
    name,           (string)
    is_public}      (Boolean, True/False)

Return Type:
    {channel_id}    (int)

Exceptions:
    InputError when: length of name is less than 1 or more than 20 characters

'''
    
    
    
    
    
    return {
        'channel_id': 1,
    }
