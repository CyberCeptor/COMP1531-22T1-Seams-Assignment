import pytest

import requests

from src import config

def test_logout_works():
    requests.delete(config.url + 'clear/v1')

    resp0 = requests.post(config.url + 'auth/register/v2', 
                  json={'email': 'abc@def.com', 'password': 'password',
                        'name_first': 'first', 'name_last': 'last'})
    register_data = resp0.json()
    token = register_data['token']

    resp1 = requests.post(config.url + 'auth/logout/v1',
                         json={'token': token})
    assert resp1.status_code == 200

# def test_users_return():
#     requests.delete(config.url + 'clear/v1')

#     resp0 = requests.post(config.url + 'auth/register/v2', 
#                   json={'email': 'abc@def.com', 'password': 'password',
#                         'name_first': 'first', 'name_last': 'last'})
#     user1 = resp0.json()
#     id1 = user1['auth_user_id']

#     resp1 = requests.post(config.url + 'auth/register/v2', 
#                   json={'email': 'def@ghi.com', 'password': 'password',
#                         'name_first': 'first', 'name_last': 'last'})
#     user2 = resp1.json()
#     id2 = user2['auth_user_id']

#     resp = requests.get(config.url + 'users/all/v1')
#     data = resp.json()
#     print(data)
#     assert len(data) == 2
#     assert data == [{
#         'u_id': id1,
#         'email': 'abc@def.com',
#         'name_first': 'first',
#         'name_last': 'last',
#         'handle_str': 'firstlast'
#         }, {
#         'u_id': id2,
#         'email': 'def@ghi.com',
#         'name_first': 'first',
#         'name_last': 'last',
#         'handle_str': 'firstlast0'
#     }]