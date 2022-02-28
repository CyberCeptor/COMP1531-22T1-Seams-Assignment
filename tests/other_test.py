import pytest

from src.auth import auth_register_v1
from src.other import clear_v1

from src.data_store import data_store
from src.channels import channels_create_v1

def test_clear_works():
    store = data_store.get()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    channels_create_v1(1, 'test_channel', True)
    assert store['users'] != []
    assert store['channels'] != []
    clear_v1()
    assert store['users'] == []
    assert store['channels'] == []

