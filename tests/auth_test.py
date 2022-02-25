import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

@pytest.fixture
def clear_and_register():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')

def test_register_invalid_email():
    # missing @ and .
    with pytest.raises(InputError):
        auth_register_v1('abc', 'password', 'first', 'last')
    clear_v1()

    # missing @
    with pytest.raises(InputError):
        auth_register_v1('abc.def', 'password', 'first', 'last')
    clear_v1()

    # missing .
    with pytest.raises(InputError):
        auth_register_v1('abc@def', 'password', 'first', 'last')
    clear_v1()

    # missing characters before @
    with pytest.raises(InputError):
        auth_register_v1('@def.com', 'password', 'first', 'last')
    clear_v1()

    # missing characters between @ and .
    with pytest.raises(InputError):
        auth_register_v1('abc@.com', 'password', 'first', 'last')
    clear_v1()

    # missing characters after .
    with pytest.raises(InputError):
        auth_register_v1('abc@def.', 'password', 'first', 'last')
    clear_v1()

    # numbers after .
    with pytest.raises(InputError):
        auth_register_v1('abc@def.123', 'password', 'first', 'last')

# based on code Haydon wrote in project starter video
def test_register_duplicate_email(clear_and_register):
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last')
    clear_v1()

def test_register_invalid_password():
    # password too short
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'pass', 'first', 'last')
    clear_v1()

    # space in password
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'pass word', 'first', 'last')
    clear_v1()

def test_register_invalid_name():
    # first name too long
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 
                        'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz', 
                        'last')
    clear_v1()

    # last name too long
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 
                        'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz')
    clear_v1()

    # first name has symbols other than - and '
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first@', 'last')
    clear_v1()

    # first name has numbers
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first1', 'last')
    clear_v1()

    # last name has symbols other than - and '
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last@')
    clear_v1()

    # last name has numbers
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last1')
    clear_v1()

# based on code Hayden wrote in project starter video
def test_register_works():
    register_return = auth_register_v1('abc@def.com', 'password', 
                                        'first', 'last')
    auth_user_id1 = register_return['auth_user_id'] 

    login_return = auth_login_v1('abc@def.com', 'password')
    auth_user_id2 = login_return['auth_user_id']   
    
    assert auth_user_id1 == auth_user_id2

def test_login_invalid(clear_and_register):
    # incorrect password
    with pytest.raises(InputError):
        auth_login_v1('abc@def.com', 'wordpass')

    # email does not belong to a user
    with pytest.raises(InputError):
        auth_login_v1('ghi@jkl.com', 'password')