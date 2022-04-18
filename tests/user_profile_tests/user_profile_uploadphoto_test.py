"""
Filename: user_profile_uploadphoto_test.py

Author: Jenson Craig Morgan z5360181, Aleesha Bunrith(z5371516)
Created: 11/04/2022

Description:

    user/profile/uploadphoto/v1

    Pytests for the user profile function uploading photos.

    Will test against all possible factors:
        - incorrect token values/types/expired_token/unsaved_token
        - image too small (e_end <= x_start or y_end <= y_start)
        - invalid image_url
        - invalid image format (not JPG)
        - any dimensions given (x_start, x_end, etc) are not within the dimensions
        of the image at the given URL
""" 

import pytest
import requests
from src import config
from src.global_vars import EXPIRED_TOKEN, UNSAVED_TOKEN, STATUS_OK, \
                            STATUS_INPUT_ERR, STATUS_ACCESS_ERR

url = 'https://static.wikia.nocookie.net/doomsday_animations/images/3/33/Pingu.jpg/revision/latest?cb=20200719151508'
#url = 'http://clipart-library.com/images/kiKB87aeT.jpg'
https_url = 'http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg'

@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_working(clear_register):
    """
    Testing the uploadphoto works correctly, changes the users profile picture 
    accordingly.
    """
    user = clear_register

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user['token'], 'u_id': user['auth_user_id']})
    assert user_profile.status_code == STATUS_OK
    profile = user_profile.json()['user']

    profile_img1 = profile['profile_img_url']

    # testing the user has a default profile picture.
    profile_picture = requests.get(profile_img1)
    assert profile_picture.status_code == STATUS_OK

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 200, 
                            'y_end': 200})
    assert image.status_code == STATUS_OK

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': https_url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 200, 
                            'y_end': 200})
    assert image.status_code == STATUS_OK

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': user['token'], 'u_id': user['auth_user_id']})
    assert user_profile.status_code == STATUS_OK
    profile = user_profile.json()['user']

    profile_img2 = profile['profile_img_url']

    # Testing the get the jpg for the account
    profile_picture = requests.get(profile_img2)
    assert profile_picture.status_code == STATUS_OK

    # Check that a get request to a file that doesnt exists returns input error.
    profile_picture2 = requests.get(config.url + 'static/2.jpg')
    assert profile_picture2.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register_two_createchanneldm')
def test_user_uploadphoto_working_in_channel_dm(clear_register_two_createchanneldm):
    """
    Testing the uploadphoto works correctly, changes the users profile picture 
    accordingly.
    """
    token = clear_register_two_createchanneldm[0]['token']
    user_id = clear_register_two_createchanneldm[0]['auth_user_id']
    chan_id = clear_register_two_createchanneldm[2]
    dm_id = clear_register_two_createchanneldm[3]

    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': token, 'u_id': user_id})
    assert user_profile.status_code == STATUS_OK
    profile = user_profile.json()['user']

    profile_img1 = profile['profile_img_url']

    # testing the user has a default profile picture.
    profile_picture = requests.get(profile_img1)
    assert profile_picture.status_code == STATUS_OK
    
    # check the channel data has the default profile picture.
    channel_details = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': chan_id})
    assert channel_details.status_code == STATUS_OK
    channel = channel_details.json()

    for user in channel['all_members']:
        if user['u_id'] == user_id:
            assert user['profile_img_url'] == profile_img1

    ### Check the DM data has the default profile picture.
    dm_details = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token, 'dm_id': dm_id})
    assert dm_details.status_code == STATUS_OK
    dm = dm_details.json()

    for user in dm['members']:
        if user['u_id'] == user_id:
            assert user['profile_img_url'] == profile_img1

    # upload a new profile image
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': token, 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 200, 
                            'y_end': 200})
    assert image.status_code == STATUS_OK


    user_profile = requests.get(config.url + 'user/profile/v1', 
                    params={'token': token, 'u_id': user_id})
    assert user_profile.status_code == STATUS_OK
    profile = user_profile.json()['user']

    profile_img2 = profile['profile_img_url']

    # Testing the get the jpg for the account
    profile_picture = requests.get(profile_img2)
    assert profile_picture.status_code == STATUS_OK

    # check the channel data has been updated with the new URL.
    channel_details = requests.get(config.url + 'channel/details/v2', 
                          params={'token': token, 'channel_id': chan_id})
    assert channel_details.status_code == STATUS_OK
    channel = channel_details.json()

    for user in channel['all_members']:
        if user['u_id'] == user_id:
            assert user['profile_img_url'] == profile_img2

    ### Check the DM data has been updated with the new URL
    dm_details = requests.get(config.url + 'dm/details/v1', 
                        params={'token': token, 'dm_id': dm_id})
    assert dm_details.status_code == STATUS_OK
    dm = dm_details.json()

    for user in dm['members']:
        if user['u_id'] == user_id:
            assert user['profile_img_url'] == profile_img2

@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_invalid_url(clear_register):
    """
    Testing the function against various invalid URL's.
        - booleans
        - integer
        - string
        - A HTTPS URL
    """
    user = clear_register

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': 'invalid_url', 
                            'x_start': 0, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': True, 
                            'x_start': 0, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': -1, 
                            'x_start': 0, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_bad_dimensions(clear_register):
    """
    Tests against invalid dimensions of the x_start, x_end, y_start, and y_end. 
    any value given is not within the dimensions of the image at the URL
    x_end <= x_start or y_end <= y_start.
    """
    user = clear_register
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 30000, 
                            'y_end': 30000})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': -1, 'y_start': -1, 'x_end': 300,
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 30000, 'y_start': 30000, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': -1, 
                            'y_end': -1})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 0, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 300, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': True, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 
                            'x_start': 'string', 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_non_jpg(clear_register):
    """
    The URL given is a link to a non JPG. 
    """
    user = clear_register
    non_jpg_url = 'http://clipart-library.com/images/qiBXRy5gT.png'
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': non_jpg_url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_invalid_token():
    """
    Tests the function agains all possible inputs for invalid tokens
    """
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': EXPIRED_TOKEN, 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_ACCESS_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': UNSAVED_TOKEN, 'img_url': url, 
                            'x_start': 0, 'y_start': 0, 'x_end': 300, 
                            'y_end': 300})
    assert image.status_code == STATUS_ACCESS_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': True, 'img_url': url, 'x_start': 0, 
                            'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': -1, 'img_url': url, 'x_start': 0, 
                            'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': 'string', 'img_url': url, 'x_start': 0, 
                            'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_ACCESS_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': '', 'img_url': url, 'x_start': 0, 
                            'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR


requests.delete(config.url + 'clear/v1')
    
