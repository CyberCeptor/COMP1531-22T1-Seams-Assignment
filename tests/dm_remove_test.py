"""
Filename: dm_remove_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: pytest for dm_remove
"""
import pytest
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1

def test_dm_remove_valid():
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm remove successfully

    Arguments: clear_and_register(fixture)

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')

    token1 = user1['token']
    token2 = user2['token']
    id1 = user1["auth_user_id"]
    id2 = user2["auth_user_id"]

    dm_dict = dm_create_v1(token2, [id1])
    dm_id = dm_dict['dm_id']
    dm_remove_v1(token2, dm_id)
    dm_dict = dm_list_v1(token2) 
    assert dm_dict['dms'] == []

    dm_dict = dm_create_v1(token1, [id2])
    dm_id = dm_dict['dm_id']
    dm_remove_v1(token1, dm_id)
    dm_dict = dm_list_v1(token1)
    assert dm_dict['dms'] == []

    dm_dict = dm_create_v1(token1, [id2,id1])
    dm_id = dm_dict['dm_id']
    dm_remove_v1(token1, dm_id)
    dm_dict = dm_list_v1(token1)
    assert dm_dict['dms'] == []

def test_dm_remove_invalid_dm():
    """
    clears any data stored in data_store and registers a user with the
    given information, raise inputerror by invalid u_id

    Arguments: clear_and_register(fixture)

    Exceptions: InputError - raised by invalid u_id

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')

    token1 = user1['token']
    id1 = user1['auth_user_id']
    id2 = user2['auth_user_id']

    dm_create_v1(token1, [id1,id2])
    with pytest.raises(InputError):
        dm_remove_v1(token1, 900)

    with pytest.raises(InputError):
        dm_remove_v1(token1, -900)
    
    with pytest.raises(InputError):
        dm_remove_v1(token1, '')

    with pytest.raises(InputError):
        dm_remove_v1(token1, False)
    
    with pytest.raises(InputError):
        dm_remove_v1(token1, 'sh')

def test_dm_remove_not_creator():
    """
    clears any data stored in data_store and registers a user with the
    given information, raise accesserror by not a creator

    Arguments: clear_and_register(fixture)

    Exceptions: AccessError - raised by not a creator

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')

    token1 = user1['token']
    token2 = user2['token']
    id1 = user1['auth_user_id']
    id2 = user2['auth_user_id']
    dm_dict = dm_create_v1(token1, [id1,id2])
    dm_id = dm_dict["dm_id"]

    with pytest.raises(AccessError):
        dm_remove_v1(token2, dm_id)
clear_v1()
'''
def test_dm_remove_not_in_dm():
    """
    clears any data stored in data_store and registers a user with the
    given information, raise accesserror by not in dm

    Arguments: clear_and_register(fixture)

    Exceptions: AccessError - raised by not in dm

    Return Value: N/A
    """
    # Clear the data structure
    clear_v1()

    # Call other functions to create the data and store in data structure
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')

    token1 = user1['token']
    id1 = user1['auth_user_id']
    id2 = user2['auth_user_id']

    dm_dict = dm_create_v1(token1, [id1,id2])
    dm_id = dm_dict['dm_id']
    dm_leave_v1(token1, dm_id)
    with pytest.raises(AccessError):
        dm_remove_v1(token1, dm_id)
'''