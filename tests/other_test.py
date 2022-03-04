"""
Filename: other_test.py

Author: group
Created: 24/02/2022 - 04/03/2022

Description: pytest for checking if clear_v1() works
"""

from src.auth import auth_register_v1
from src.other import clear_v1
from src.channels import channels_create_v1
from src.data_store import data_store

def test_clear_works():
    """ checks if all stored data is gone once clear_v1 is called

    Arguments: N/A

    Exceptions: N/A

    Return Value: N/A """

    store = data_store.get()
    auth_register_v1('abc@defg.com', 'password', 'first', 'last')
    channels_create_v1(1, 'test_channel', True)
    assert store['users'] != []
    assert store['channels'] != []
    clear_v1()
    assert store['users'] == []
    assert store['channels'] == []
