import pytest
import requests
from src import config

@pytest.fixture(name='clear_and_register')
def fixture_clear_and_register():
    """
    clears any data stored in data_store and registers a user with the
    given information

    Arguments: N/A

    Exceptions: N/A

    Return Value: data['token']
                  data['auth_user_id']
    """
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'wky@gmail.com', 'password': '547832',
                                'name_first': 'wang', 'name_last': 'kaiyan'})
    data = resp.json()
    return [data['token'], data['auth_user_id']]

def test_dm_create_valid(clear_and_register):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A
    """

    token1 = clear_and_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    data2 = resp2.json()
    id2 = data1['auth_user_id']
    id3 = data2['auth_user_id']

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2]})
    assert create.status_code == 200

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2,id3]})
    assert create.status_code == 200

def test_dm_create_invalid_uid(clear_and_register):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: N/A

    Exceptions: InputError - raised by invalid ids

    Return Value: N/A
    """
    token1 = clear_and_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    id1 = data1['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,-500]})
    assert create.status_code == 400
    
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,500]})
    assert create.status_code == 403

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,True]})
    assert create.status_code == 400

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,'s']})
    assert create.status_code == 400

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id1,'']})
    assert create.status_code == 400

    create = requests.post(config.url + 'dm/create/v1',
                        json={'token': token1, 'u_ids': ['j',id1]})
    assert create.status_code == 400

def test_dm_create_duplicate_uid(clear_and_register):
    """
    clears any data stored in data_store and registers users with the
    given information, create the dm with token and u_ids

    Arguments: N/A

    Exceptions: InputError - raised by duplicate ids

    Return Value: N/A
    """
    token1 = clear_and_register[0]
    resp1 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'lmz@gmail.com', 'password': '893621',
                                'name_first': 'li', 'name_last': 'mingzhe'})
    data1 = resp1.json()
    resp2 = requests.post(config.url + 'auth/register/v2', 
                        json={'email': 'hyf@gmail.com', 'password': 'hyf1234',
                                'name_first': 'huang', 'name_last': 'yifei'})
    data2 = resp2.json()
    id2 = data1['auth_user_id']
    id3 = data2['auth_user_id']
    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id2,id2]})
    assert create.status_code == 400

    create = requests.post(config.url + 'dm/create/v1', 
                        json={'token': token1, 'u_ids': [id3,id3]})
    assert create.status_code == 400

requests.delete(config.url + 'clear/v1')