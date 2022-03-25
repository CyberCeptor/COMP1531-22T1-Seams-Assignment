"""
Filename: dm_list_test.py

Author: Zefan Cao(z5237177)
Created: 14/03/2022 - 24/03/2022

Description: pytest for dm_list
"""
from src.error import InputError, AccessError
from src.other import clear_v1
from src.dm import dm_create_v1, dm_list_v1
from src.auth import auth_register_v2
def test_dm_list_valid():
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids, list with token

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

    dm_create_v1(token1, [id2])
    dm_dict = dm_list_v1(token1)
    assert len(dm_dict['dms']) == 1
    assert dm_dict['dms'] == [{'dm_id':1, 'name': 'limingzhe, wangkaiyan'}]

    dm_create_v1(token1, [id3])
    dm_dict = dm_list_v1(token1)
    assert len(dm_dict["dms"]) == 2
    assert dm_dict["dms"] == [{'dm_id':1, 'name': 'limingzhe, wangkaiyan'}, 
    {'dm_id':2, 'name': 'huangyifei, wangkaiyan'}]
clear_v1()