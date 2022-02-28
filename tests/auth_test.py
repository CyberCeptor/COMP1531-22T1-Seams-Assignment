
import pytest

from src.auth import auth_register_v1
from src.auth import auth_login_v1
from src.error import InputError
from src.other import clear_v1

from src.data_store import data_store

@pytest.fixture
def clear_and_register():
    clear_v1()
    auth_register_v1('abc@def.com', 'password', 'first', 'last')

@pytest.fixture
def store_users():
    clear_v1()
    store = data_store.get()
    users = store['users']
    return users

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

def test_register_invalid_name():
    # first name too short
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', '', 'last')
    clear_v1()

    # last name too short
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', '')
    clear_v1()

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

    # first name has symbols other than - and ' and spaces
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first@', 'last')
    clear_v1()

    # first name has numbers
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first1', 'last')
    clear_v1()

    # last name has symbols other than - and ' and spaces
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last@')
    clear_v1()

    # last name has numbers
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', 'first', 'last1')
    clear_v1()

    # name has no letters -> would create an empty handle
    with pytest.raises(InputError):
        auth_register_v1('abc@def.com', 'password', '-', ' ')
    clear_v1()

# based on code Hayden wrote in project starter video
def test_register_works():
    clear_v1()
    register_return = auth_register_v1('abc@def.com', 'password', 
                                        'first', 'last')
    auth_user_id1 = register_return['auth_user_id'] 

    login_return = auth_login_v1('abc@def.com', 'password')
    auth_user_id2 = login_return['auth_user_id']
    
    assert auth_user_id1 == auth_user_id2

def test_handle_creation_invalid_symbols(store_users):
    # first name has symbols
    auth_register_v1('abc@def.com', 'password', "f'irst-fir st", 'last')
    handle0 = store_users[0]['handle']
    assert handle0 == 'firstfirstlast'

    # last name has symbols
    auth_register_v1('abc@def.co', 'password', 'first', "la'st-la st")
    handle1 = store_users[1]['handle']
    assert handle1 == 'firstlastlast'

def test_handle_creation_capitals(store_users):
    # first name has capitals
    auth_register_v1('abc@def.com', 'password', 'FIRST', 'last')
    handle0 = store_users[0]['handle']
    assert handle0 == 'firstlast'

    # last name has capitals
    auth_register_v1('abc@def.co', 'password', 'first', 'LASTY')
    handle1 = store_users[1]['handle']
    assert handle1 == 'firstlasty'

    # both names have capitals
    auth_register_v1('abc@de.co', 'password', 'firST', 'LAStee')
    handle2 = store_users[2]['handle']
    assert handle2 == 'firstlastee'

def test_handle_creation_invalid_length(store_users):
    # first name longer than 20 characters
    auth_register_v1('abc@def.com', 'password', 'abcdefghijklmnopqrstuvwxyz', 
                    'last')
    handle0 = store_users[0]['handle']
    assert handle0 == 'abcdefghijklmnopqrst'

    # last name longer than 20 characters
    auth_register_v1('abc@def.co', 'password', 'first', 
                    'abcdefghijklmnopqrstuvwxyz')
    handle1 = store_users[1]['handle']
    assert handle1 == 'firstabcdefghijklmno'

    # name longer than 20 characters
    auth_register_v1('abc@de.com', 'password', 'abcdefghijklmnopqr', 'last')
    handle2 = store_users[2]['handle']
    assert handle2 == 'abcdefghijklmnopqrla'

def test_handle_creation_duplicates(store_users):
    auth_register_v1('abc@def.com', 'password', 'first', 'last')
    handle0 = store_users[0]['handle']
    assert handle0 == 'firstlast'

    auth_register_v1('abc@def.co', 'password', 'first', 'last')
    handle1 = store_users[1]['handle']
    assert handle1 == 'firstlast0'

def test_handle_creation_invalid_length_duplicates(store_users):
    auth_register_v1('abc@def.com', 'password', 'abcdefghijklmnopqr', 'last')
    handle0 = store_users[0]['handle']
    assert handle0 == 'abcdefghijklmnopqrla'

    auth_register_v1('abc@def.co', 'password', 'abcdefghijklmnopqr', 'last')
    handle1 = store_users[1]['handle']
    assert handle1 == 'abcdefghijklmnopqrla0'

    assert len(handle0) != len(handle1)

def test_login_invalid(clear_and_register):
    # email does not belong to a user
    with pytest.raises(InputError):
        auth_login_v1('ghi@jkl.com', 'password')
    
    # incorrect password
    with pytest.raises(InputError):
        auth_login_v1('abc@def.com', 'wordpass')
<<<<<<< HEAD

=======
    clear_v1()
>>>>>>> 40128b7079dfcdc985001ab5a5ddf76b609586a0
