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

    resp1 = requests.post(config.url + 'auth/logout/v2',
                         json={'token': token})
    assert resp1.status_code == 200