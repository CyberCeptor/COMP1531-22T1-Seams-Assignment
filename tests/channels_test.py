
import pytest
from src.auth import auth_register_v1
from src.auth import channels_create_v1

from src.auth import channels_list_v1
from src.auth import channels_linstall_v1

from src.auth import channel_details_v1
from src.auth import channel_join_v1
from src.auth import channel_invite_v1
from src.auth import channel_messages_v1

from src.auth import clear_v1
from src.error import InputError



from src.auth import auth_login_v1

# length of name is less than 1 or more than 20 characters
def test_channels_create_too_short():
    clear_v1()
    channel = auth_register_v1('abc@def.com', 'password', 'first', 'last')

    with pytest.raises(InputError):
        channels_create_v1('auth_user_id', '', 'is_public')

def test_channels_create_too_long():
    clear_v1()
    channel = auth_register_v1('abc@def.com', 'password', 'first', 'last')

    with pytest.raises(InputError):
        channels_create_v1('auth_user_id', 'MoreThan20Characters!', 'is_public')



def test_channels_list_v1():
    clear_v1()
    channel1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')




