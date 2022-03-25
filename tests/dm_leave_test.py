"""
Filename: dm_leave_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: http pytest for dm_leave
"""
import pytest
from src.dm import dm_create_v1, dm_leave_v1, dm_details_v1
from src.auth import auth_register_v2
from src.error import InputError, AccessError
from src.other import clear_v1
def test_dm_leave_valid():
    """
    clears any data stored in data_store and registers a user with the
    given information, run dm details successful

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')
    token1 = user1['token']
    token2 = user2['token']
    id2 = user2['auth_user_id']
    id1 = user1['auth_user_id']
    dm_dict = dm_create_v1(token1, [id2])
    dm_id = dm_dict['dm_id']
    dm_leave_v1(token2, dm_id)
    detail = dm_details_v1(token1, dm_id)
    assert detail['members'] == [{
        'u_id':id1,
        'email':'wky@gmail.com',
        'name_first':'wang',
        'name_last':'kaiyan',
        'handle_str':'wangkaiyan'
    }]

def test_dm_leave_invalid_dm():
    """
    clears any data stored in data_store and registers a user with the
    given information, raised a inputerror by invalid dm id

    Arguments: clear_and_register(fixture)

    Exceptions: InputErroe - raised by invalid dm_id

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')

    token1 = user1['token']
    id2 = user2['auth_user_id']
    dm_create_v1(token1, [id2])
    with pytest.raises(InputError):
        dm_leave_v1(token1, 900)

    with pytest.raises(InputError):
        dm_leave_v1(token1, -900)
    
    with pytest.raises(InputError):
        dm_leave_v1(token1, '')

    with pytest.raises(InputError):
        dm_leave_v1(token1, True)
    
    with pytest.raises(InputError):
        dm_leave_v1(token1, 'sh')

def test_dm_leave_auth_notin_dm():
    """
    clears any data stored in data_store and registers a user with the
    given information, raise a access error by the auth not in dm

    Arguments: clear_and_register(fixture)

    Exceptions: AccessError - raised by auth not in dm

    Return Value: N/A
    """
    clear_v1()
    user1 = auth_register_v2('wky@gmail.com', '547832', 'wang', 'kaiyan')
    user2 = auth_register_v2('lmz@gmail.com', '893621', 'li', 'mingzhe')
    user3 = auth_register_v2('hyf@gmail.com', 'hyf1234', 'huang', 'yifei')
    token1 = user1['token']
    token3 = user3['token']
    id2 = user2['auth_user_id']
    dm_dict = dm_create_v1(token1, [id2])
    dm_id = dm_dict["dm_id"]
    with pytest.raises(AccessError):
        dm_leave_v1(token3, dm_id)
clear_v1()