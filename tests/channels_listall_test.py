# """
# Filename: channels_test.py

# Author: Yangjun Yue(5317840)
# Created: 28/02/2022 - 04/03/2022

# Description: pytests for channel_listall_v1
# """

# import pytest

# from src.auth import auth_register_v1

# from src.other import clear_v1
# from src.error import InputError, AccessError

# from src.channels import channels_create_v1, channels_listall_v1

# @pytest.fixture(name='clear_and_register_and_create')
# def fixture_clear_and_register_and_create():
#     """
#     Clears any data stored in data_store and registers a user with the
#     given information, create a channel using user id

#     Arguments: N/A

#     Exceptions: N/A

#     Return Value: N/A
#     """

#     clear_v1()
#     user1 = auth_register_v1('abc@def.com', 'password', 'first', 'last')
#     chan_id1 = channels_create_v1(1, 'channel_name', True)
#     return [user1['auth_user_id'], chan_id1['channel_id']]

# def test_channels_listall_invalid_user_id(clear_and_register_and_create):
#     """
#     Testing invalid user id to raise input error

#     Arguments: clear_and_register_and_create (fixture)

#     Exceptions:
#         InputError - non existing user id

#     Return Value: N/A
#     """
#     # pylint: disable=unused-argument

#     with pytest.raises(InputError):
#         channels_listall_v1(-1)
#     with pytest.raises(AccessError):
#         channels_listall_v1(2)
#     with pytest.raises(InputError):
#         channels_listall_v1('4')
#     with pytest.raises(InputError):
#         channels_listall_v1('not int')
#     with pytest.raises(InputError):
#         channels_listall_v1(True)

# # testing if return values are the right type
# def test_channels_listall_v1_return(clear_and_register_and_create):
#     """ testing if listall returns right type of value

#     Arguments: clear_and_register_and_create (fixture)

#     Exceptions: N/A

#     Return Value: N/A
#     """

#     # pylint: disable=unused-argument
#     id1 = clear_and_register_and_create[0]
#     chan_id1 = clear_and_register_and_create[1]
#     result = channels_listall_v1(id1)
#     # result is a list of dictionary
#     # check if first dictionary gives the right values
#     assert result['channels'][0] == {
#         "channel_id": chan_id1,
#         "name": 'channel_name',
#     }

# clear_v1()