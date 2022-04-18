"""
Filename: standup_send_http_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http test for standup_send
"""

import pytest
import time
import requests
from src import config
from src.global_vars import STATUS_OK, STATUS_INPUT_ERR, STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_standup_send_valid(clear_register_createchannel):
    """
    clears any data stored in data_store and registers users with the
    given information, test standup send valid
    """
    user1 = clear_register_createchannel[0]
    token = user1['token']
    channel_id = clear_register_createchannel[1]
    
    requests.post(config.url + 'standup/start/v1',
                json={'token': token, 'channel_id': channel_id,
                    'length': 1})

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': channel_id,
                            'message': 'hello world'})
    assert stand.status_code == STATUS_OK

    time.sleep(2)
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': channel_id, 
                                    'start': 0})
    info = resp1.json()
    assert(len(info['messages']) == 1)
    assert info['messages'][0]['message'] == 'firstlast: hello world'
    
@pytest.mark.usefixtures('clear_register')
def test_standup_send_invalid_channel(clear_register):
    """
    clears any data stored in data_store and registers users with the
    given information, a inputerror raised by invalid channel
    """
    user1 = clear_register
    token = user1['token']

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': 44,
                            'message': 'hello world'})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': -44,
                            'message': 'hello world'})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': False,
                            'message': 'hello world'})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': '',
                            'message': 'hello world'})
    assert stand.status_code == STATUS_INPUT_ERR

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': 'ahs',
                            'message': 'hello world'})
    assert stand.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_standup_send_invalid_message(clear_register_createchannel):
    """
    clears any data stored in data_store and registers users with the
    given information, a input error raised by invalid message
    """
    user1 = clear_register_createchannel[0]
    token = user1['token']
    channel_id = clear_register_createchannel[1]

    requests.post(config.url + 'standup/start/v1',
                json={'token': token, 'channel_id': channel_id,
                    'length': 1})

    message = 'hello' *201
    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': channel_id,
                            'message': message})
    assert stand.status_code ==  STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_standup_send_standup_not_running(clear_register_createchannel):
    """
    clears any data stored in data_store and registers users with the
    given information, a input error raised by a standup is not running
    """
    user1 = clear_register_createchannel[0]
    token = user1['token']
    channel_id = clear_register_createchannel[1]

    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': channel_id,
                            'message': 'hello world'})
    assert stand.status_code ==  STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two')
def test_standup_start_is_not_in_channel(clear_register_two):
    """
    clears any data stored in data_store and registers users with the
    given information, a access error raised by user is not in channel
    """
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]
    token1 = user1['token']
    token2 = user2['token']
    chan = requests.post(config.url + 'channels/create/v2',
                        json={'token': token1, 'name': 'channel_name',
                            'is_public': True})
    chan_data = chan.json()
    channel_id = chan_data['channel_id']
    
    requests.post(config.url + 'standup/start/v1',
                json={'token': token1, 'channel_id': channel_id,
                    'length': 1})
    
    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token2, 'channel_id': channel_id,
                            'message': 'hello world'})
    assert stand.status_code == STATUS_ACCESS_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_standup_send_invalid_messages(clear_register_createchannel):
    """
    clears any data stored in data_store and registers users with the
    given information, test invalid message
    """
    user1 = clear_register_createchannel[0]
    token = user1['token']
    channel_id = clear_register_createchannel[1]

    requests.post(config.url + 'standup/start/v1',
                json={'token': token, 'channel_id': channel_id,
                    'length': 1})

    message = [2]
    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': channel_id,
                            'message': message})
    assert stand.status_code == STATUS_INPUT_ERR

    message = ''
    stand = requests.post(config.url + 'standup/send/v1',
                        json={'token': token, 'channel_id': channel_id,
                            'message': message})
    assert stand.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_createchannel')
def test_standup_send_no_messages(clear_register_createchannel):
    """
    check that a standup message is not sent if there are no messages sent 
    during the standup
    """
    user1 = clear_register_createchannel[0]
    token = user1['token']
    channel_id = clear_register_createchannel[1]
    
    resp0 = requests.post(config.url + 'standup/start/v1',
                json={'token': token, 'channel_id': channel_id,
                    'length': 1})
    assert resp0.status_code == STATUS_OK

    time.sleep(2)
    resp1 = requests.get(config.url + 'channel/messages/v2', 
                          params = {'token': token, 'channel_id': channel_id, 
                                    'start': 0})
    assert resp0.status_code == STATUS_OK
    
    info = resp1.json()
    assert(len(info['messages']) == 0)


requests.delete(config.url + 'clear/v1')