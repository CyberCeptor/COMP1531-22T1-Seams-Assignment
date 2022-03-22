"""
Filename: channels_test.py

Author: Yangjun Yue(5317840)
Created: 28/02/2022 - 04/03/2022

Description: pytests for channel_listall_v1
"""

import pytest
import requests
from src.auth import auth_register_v1

from src.other import clear_v1
from src.error import InputError, AccessError

from src.channels import channels_create_v1, channels_listall_v1
from src import config


@pytest.fixture(name='clear_and_register_and_create')
def fixture_clear_and_register_and_create():
    """
    Clears any data stored in data_store and registers a user with the
    given information, create a channel using user id

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    # clear_v1()
    # user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
    # chan_id1 = channels_create_v1(1, 'channel_name', True)
    # return [user1['auth_user_id'], chan_id1['channel_id']]
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                         json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user_data = resp.json()
    token = user_data['token']
    u_id = user_data['auth_user_id']
    resp_1 = requests.post(config.url + 'channels/create/v2',
                            json={'token': token, 'name': 'channel_name',
                                    'is_public': True})
    channel_data = resp_1.json()
    channel_id = channel_data['channel_id']
    
    return [token, channel_id, u_id]

def test_channels_listall_invalid_token(clear_and_register_and_create):
    """
    Testing invalid user id to raise input error

    Arguments: clear_and_register_and_create (fixture)

    Exceptions:
        InputError - non existing user id

    Return Value: N/A
    """
    # pylint: disable=unused-argument

    # with pytest.raises(InputError):
    #     channels_listall_v1(-1)
    # with pytest.raises(AccessError):
    #     channels_listall_v1(2)
    # with pytest.raises(InputError):
    #     channels_listall_v1('4')
    # with pytest.raises(InputError):
    #     channels_listall_v1('not int')
    # with pytest.raises(InputError):
    #     channels_listall_v1(True)
     # passing incorrect string as token.

    # token is int
    channels_listall = requests.get(config.url + 'channels/listall/v2', params = {'token': 0})
    assert channels_listall.status_code == 400

    # token is bool
    channels_listall = requests.get(config.url + 'channels/listall/v2', params = {'token': True})
    assert channels_listall.status_code == 400
    
    channels_listall = requests.get(config.url + 'channels/listall/v2', params = {'token': False})
    assert channels_listall.status_code == 400

    # wrong string to raise access error
    channels_listall = requests.get(config.url + 'channels/listall/v2', params = {'token': 'str'})
    assert channels_listall.status_code == 403 

    # token is expired
    expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic2Vzc2lvbl9pZCI6MSwiaGFuZGxlIjoiZmly\
        c3RsYXN0IiwiZXhwIjoxNTQ3OTc3ODgwfQ.366QLXfCURopcjJbAheQYLVNlGLX_INKVwr8_TVXYEQ'

    channels_list_json = requests.get(config.url + 'channels/listall/v2', params = {'token': expired_token})
    assert channels_list_json.status_code == 403




def test_channels_listall_v1_return():
    """ testing if listall returns right type of value

    Arguments: clear_and_register_and_create (fixture)

    Exceptions: N/A

    Return Value: N/A
    """

    # pylint: disable=unused-argument

    requests.delete(config.url + 'clear/v1')
    
    # create user1
    user1 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'abc@def.com', 'password': 'password',
                               'name_first': 'first', 'name_last': 'last'})
    user1_json = user1.json()

    # create user2
    user2 = requests.post(config.url + 'auth/register/v2', 
                            json={'email': 'def@abc.com', 'password': 'password',
                               'name_first': 'first2', 'name_last': 'last2'}) 
    user2_json = user2.json()

    # create the 3 channels for user1
    channel1 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name1', 'is_public': True})

    assert channel1.status_code == 200
    channel1_json = channel1.json()

    channel2 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'channel_name2', 'is_public': True})
    channel2_json = channel2.json()

    # 3rd channel is private
    channel3 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1_json['token'], 'name': 'private_channel1', 'is_public': False})
    channel3_json = channel3.json()

    
    # create public channel for user2
    channel4 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_json['token'], 'name': 'pub_channel_user2', 'is_public': True})
    channel4_json = channel4.json()

    # create private channel for user2
    channel5 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user2_json['token'], 'name': 'pri_channel_user2', 'is_public': False})
    channel5_json = channel5.json()

    # channel_list for user 1, should return all channels
    channels_listall = requests.get(config.url + 'channels/listall/v2', params = {'token': user1_json['token']})
    channels_listall_json = channels_listall.json()


    # check the channels_list function has worked.
    assert channels_listall.status_code == 200
    # check the number of channels is all channels
    assert len(channels_listall_json['channels']) == 5
    # check that the channel_list info matches what was created.
    assert channels_listall_json['channels'][0]['channel_id'] == channel1_json['channel_id']
    assert channels_listall_json['channels'][1]['channel_id'] == channel2_json['channel_id']
    assert channels_listall_json['channels'][2]['channel_id'] == channel3_json['channel_id']
    assert channels_listall_json['channels'][3]['channel_id'] == channel4_json['channel_id']
    assert channels_listall_json['channels'][4]['channel_id'] == channel5_json['channel_id']
    assert channels_listall_json['channels'][0]['name'] == 'channel_name1'
    assert channels_listall_json['channels'][1]['name'] == 'channel_name2'
    assert channels_listall_json['channels'][2]['name'] == 'private_channel1'
    assert channels_listall_json['channels'][3]['name'] == 'pub_channel_user2'
    assert channels_listall_json['channels'][4]['name'] == 'pri_channel_user2'

    # check for user 2
    channels_listall_2 = requests.get(config.url + 'channels/listall/v2', params = {'token': user2_json['token']})
    channels_listall_2_json = channels_listall_2.json()

    assert channels_listall_2.status_code == 200
    # check the number of channels is all channels
    assert len(channels_listall_2_json['channels']) == 5
    # check that the channel_list info matches what was created.
    assert channels_listall_2_json['channels'][0]['channel_id'] == channel1_json['channel_id']
    assert channels_listall_2_json['channels'][1]['channel_id'] == channel2_json['channel_id']
    assert channels_listall_2_json['channels'][2]['channel_id'] == channel3_json['channel_id']
    assert channels_listall_2_json['channels'][3]['channel_id'] == channel4_json['channel_id']
    assert channels_listall_2_json['channels'][4]['channel_id'] == channel5_json['channel_id']
    assert channels_listall_2_json['channels'][0]['name'] == 'channel_name1'
    assert channels_listall_2_json['channels'][1]['name'] == 'channel_name2'
    assert channels_listall_2_json['channels'][2]['name'] == 'private_channel1'
    assert channels_listall_2_json['channels'][3]['name'] == 'pub_channel_user2'
    assert channels_listall_2_json['channels'][4]['name'] == 'pri_channel_user2'

    # id1 = clear_and_register_and_create[0]
    # chan_id1 = clear_and_register_and_create[1]
    # result = channels_listall_v1(id1)
    # # result is a list of dictionary
    # # check if first dictionary gives the right values
    # assert result['channels'][0] == {
    #     "channel_id": chan_id1,
    #     "name": 'channel_name',
    # }
requests.delete(config.url + 'clear/v1')
# clear_v1()

    

    

    



    
