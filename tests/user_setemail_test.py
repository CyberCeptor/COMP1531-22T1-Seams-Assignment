import pytest
import requests

from src import config
from src.global_vars import expired_token, unsaved_token

@pytest.mark.usefixtures('clear_register_two')
def test_user_setemail_working(clear_register_two):
    """
    Create 2 users,
    create a channel for user1,
    user2 joins the channel,
    user2 is added as an owner_member,
    change the emails of both users with setemail,
    assert the channel information has changed.
    """
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # create a channel, add the other user as an owner aswell, 
    # to Test that all information is updated
    channel1 = requests.post(config.url + 'channels/create/v2', 
                            json={'token': user1['token'], 'name': 'channel_name', 'is_public': True})
    assert channel1.status_code == 200
    channel1 = channel1.json()
    channel_id = channel1['channel_id']

    # Add the 2nd user to the channel
    join = requests.post(config.url + 'channel/join/v2',
                        json={'token': user2['token'], 'channel_id': channel_id})
    assert join.status_code == 200


    # add them as an owner of the channel
    addowner = requests.post(config.url + 'channel/addowner/v1',
                        json={'token': user1['token'], 'channel_id': channel_id, 'u_id': user2['auth_user_id']})
    assert addowner.status_code == 200

    # create a dm, add the other user as a member, 
    # to Test that all information is updated
    dm1 = requests.post(config.url + 'dm/create/v1', 
                             json={'token': user1['token'],
                                   'u_ids': [user2['auth_user_id']]})
    assert dm1.status_code == 200
    dm1_json = dm1.json()
    dm_id = dm1_json['dm_id']

    # changing the email address of both users.
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 'abc3@def.com'})
    assert setemail.status_code == 200

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user2['token'], 'email': 'abc4@def.com'})
    assert setemail.status_code == 200

    # test using the email that user1 previously had.
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user2['token'], 'email': 'abc@def.com'})
    assert setemail.status_code == 200

    # Assert that the all_members and owner_members channel email has also been updated
    # check the data in the channel is correct
    channel_details = requests.get(config.url + 'channel/details/v2', 
                            params={'token': user1['token'], 'channel_id': channel1['channel_id']})
    channel_json = channel_details.json()

    assert len(channel_json['owner_members']) == 2
    assert len(channel_json['all_members']) == 2

    assert 'abc3@def.com' in [k['email'] for k in channel_json['owner_members']]
    assert 'abc3@def.com' in [k['email'] for k in channel_json['all_members']]

    assert 'abc@def.com' in [k['email'] for k in channel_json['owner_members']]
    assert 'abc@def.com' in [k['email'] for k in channel_json['all_members']]

    # Assert that the all_members and owner_members channel email has also been updated
    # check the data in the channel is correct
    requests.get(config.url + 'dm/details/v1', 
                    params={'token': user1['token'], 'dm_id': dm_id})

@pytest.mark.usefixtures('clear_register_two')
def test_user_setemail_bad_email(clear_register_two):
    """
    Tests:
        - another user's email address
        - a string
        - an empty string
        - boolean
        - int/negative int
    """
    user1 = clear_register_two[0]
    user2 = clear_register_two[1]

    # test another users email
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 'def@ghi.com'})
    assert setemail.status_code == 400

    # test another users email with 2nd user
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user2['token'], 'email': 'abc@def.com'})
    assert setemail.status_code == 400

    # test bad string
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 'abcdef.com'})
    assert setemail.status_code == 400

    # test empty string
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': ''})
    assert setemail.status_code == 400

    # test boolean 
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': True})
    assert setemail.status_code == 400

    # test int
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': 1})
    assert setemail.status_code == 400

    # test negative int
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': user1['token'], 'email': -1})
    assert setemail.status_code == 400


@pytest.mark.usefixtures('clear_register')
def test_user_setemail_bad_token(clear_register):
    """
    Tests:
        - a string
        - an empty string
        - boolean
        - int/negative int
        - an expired token
        - an unsaved token
    """
    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': '', 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': 'string', 'email': 'abc2@def.com'})
    assert setemail.status_code == 403

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': 444, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': -1, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': True, 'email': 'abc2@def.com'})
    assert setemail.status_code == 400

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': expired_token, 'email': 'abc2@def.com'})
    assert setemail.status_code == 403

    setemail = requests.put(config.url + 'user/profile/setemail/v1', 
                            json={'token': unsaved_token, 'email': 'abc2@def.com'})
    assert setemail.status_code == 403
