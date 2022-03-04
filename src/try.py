from data_store import data_store
store = data_store.get()
user_dict = {"id": u_id, "email": email, "pw": password, 
                "first": name_first, "last": name_last, "handle": handle}
store['users'].append(user_dict)


print(store)


#
def test_channel_join_flockr_owner_joins_private_channel():
    clear_v1()
    store = data_store.get()
    inviter_info = auth_register_v1('wangkaiyan233@gmail.com', 'wky19991123', 'Wang', 'kaiyan')
    invitee_info = auth_register_v1('xuezhiqian234@gmail.com', 'xzq19991123', 'Xue', 'zhiqian')
    newchannel = channels_create_v1(inviter_info['auth_user_id'], 'validchannelname', False)
    channel_join_v1(inviter_info['auth_user_id'], newchannel['channel_id'])
    assert len(store['channels'][0]['members']) == 2

    '' Failure first
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            snumber = channel['is_public']
        raise InputError('Channel is invalid')
    if snumber == False:
        raise AccessError('Channel is private')
    return
    '''
    '''
    snumber = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            if channel['is_public'] == True:
                snumber = True
        raise InputError('Channel is invalid')
    if snumber == False:
        raise AccessError('Channel is private')
    return
    
    '''
