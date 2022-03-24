"""
Filename: dm_create_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: pytest for dm_create
"""
import pytest
from src.error import InputError, AccessError
from src.other import clear_v1
from src.dm import dm_create_v1
from src.auth import auth_register_v2

def test_dm_create_valid():
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')
    user3 = auth_register_v2('hyf@gmail.com', 'hyf1234', 'huang', 'yifei')

    token1 = user1['token']
    id2 = user2['auth_user_id']
    id3 = user3['auth_user_id']

    dm_dict = dm_create_v1(token1, [id2])
    assert dm_dict['dm_id'] == 1
    
    dm_dict = dm_create_v1(token1, [id2, id3])
    assert dm_dict['dm_id'] == 2

def test_dm_create_invalid_uid():
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: N/A

    Exceptions: InputError - raised by invalid u_id

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')
    token1 = user1['token']
    id2 = user2['auth_user_id']
    
    with pytest.raises(InputError):
        dm_create_v1(token1, [id2, -500])
    
    with pytest.raises(InputError):
        dm_create_v1(token1, [id2, 500])

    with pytest.raises(InputError):
        dm_create_v1(token1, [id2, ''])
    
    with pytest.raises(InputError):
        dm_create_v1(token1, [id2, True])

    with pytest.raises(InputError):
        dm_create_v1(token1, [id2, 's'])

    with pytest.raises(InputError):
        dm_create_v1(token1, ['a', id2])

def test_dm_create_duplicate_uid():
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: N/A

    Exceptions: InputError - raised by duplicate ids

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')
    user3 = auth_register_v2('hyf@gmail.com', 'hyf1234', 'huang', 'yifei')
    token1 = user1['token']
    id2 = user2['auth_user_id']
    id3 = user3['auth_user_id']
    with pytest.raises(InputError):
        dm_create_v1(token1, [id2, id2])
    
    with pytest.raises(InputError):
        dm_create_v1(token1, [id3, id3])
clear_v1()