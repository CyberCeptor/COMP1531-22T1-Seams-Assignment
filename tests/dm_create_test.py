from lib2to3.pgen2 import token
import pytest
from src.error import InputError, AccessError
from src.other import clear_v1
from src.dm import dm_create_v1
from src.auth import auth_register_v1

def test_dm_create_valid():
    """
    This function checks valid case where dm channel
    is created successfully.
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    user1 = auth_register_v1('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v1('lmz@gmail.com', '893621', 'li', 'mingzhe')
    user3 = auth_register_v1('hyf@gmail.com', 'hyf1234', 'huang', 'yifei')

    token = user1['token']
    id2 = user2['auth_user_id']
    id3 = user3['auth_user_id']

    dm_dict = dm_create_v1(token, [id2])
    assert dm_dict['dm_id'] == 1
   
    dm_dict = dm_create_v1(token, [id2, id3])
    assert dm_dict['dm_id'] == 2

def test_dm_create_invalid_uid():
    """
    This function test for invalid u_id in the input
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    user1 = auth_register_v1('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v1('lmz@gmail.com', '893621', 'li', 'mingzhe')
    token = user1['token']
    id2 = user2['auth_user_id']
    
    with pytest.raises(InputError):
        dm_create_v1(token, [id2, -500])
    
    with pytest.raises(AccessError):
        dm_create_v1(token, [id2, 500])

    with pytest.raises(InputError):
        dm_create_v1(token, [id2, ''])
    
    with pytest.raises(InputError):
        dm_create_v1(token, [id2, True])

    with pytest.raises(InputError):
        dm_create_v1(token, [id2, 's'])

    with pytest.raises(InputError):
        dm_create_v1(token, ['a', id2])

def test_dm_create_duplicate_uid():
    """
    This function test for invalid u_id in the input
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    user1 = auth_register_v1('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v1('lmz@gmail.com', '893621', 'li', 'mingzhe')
    token = user1['token']
    id2 = user2['auth_user_id']
    with pytest.raises(InputError):
        dm_create_v1(token, [id2, id2])

clear_v1()