import pytest

from src.auth import auth_register_v1
from src.other import clear_v1

from src.data_store import data_store

def test_clear_works():
    store = data_store.get()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    clear_v1()
    assert store['users'] == []
    