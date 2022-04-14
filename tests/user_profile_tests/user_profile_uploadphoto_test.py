"""
Filename: user_profile_uploadphoto_test.py

Author: Jenson Craig Morgan z5360181
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

url = 'http://clipart-library.com/images/kiKB87aeT.jpg'
https_url = 'http://cdn.mos.cms.futurecdn.net/iC7HBvohbJqExqvbKcV3pP.jpg'

@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_working(clear_register):
    """
    Testing the uploadphoto works correctly, changes the users profile picture accordingly.
    """
    user = clear_register
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 200, 'y_end': 200})
    assert image.status_code == STATUS_OK

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': https_url, 'x_start': 0, 'y_start': 0, 'x_end': 200, 'y_end': 200})
    assert image.status_code == STATUS_OK


    # Testing the get the jpg for the account
    profile_picture = requests.get(config.url + 'static/1.jpg')
    assert profile_picture.status_code == STATUS_OK

    profile_picture = requests.get(config.url + 'static/2.jpg')
    assert profile_picture.status_code == STATUS_INPUT_ERR







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
                        json={'token': user['token'], 'img_url': 'invalid_url', 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': True, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': -1, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
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
                        json={'token': user['token'], 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 30000, 'y_end': 30000})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': -1, 'y_start': -1, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': 30000, 'y_start': 30000, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': -1, 'y_end': -1})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 0, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': 300, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': True, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': url, 'x_start': 'string', 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR


@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_non_jpg(clear_register):
    """
    The URL given is a link to a non JPG. 
    """
    user = clear_register
    non_jpg_url = 'http://clipart-library.com/images/qiBXRy5gT.png'
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': user['token'], 'img_url': non_jpg_url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR


@pytest.mark.usefixtures('clear_register')
def test_user_uploadphoto_invalid_token():
    """
    Tests the function agains all possible inputs for invalid tokens
    """
    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': EXPIRED_TOKEN, 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_ACCESS_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': UNSAVED_TOKEN, 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_ACCESS_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': True, 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': -1, 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': 'string', 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_ACCESS_ERR

    image = requests.post(config.url + 'user/profile/uploadphoto/v1', 
                        json={'token': '', 'img_url': url, 'x_start': 0, 'y_start': 0, 'x_end': 300, 'y_end': 300})
    assert image.status_code == STATUS_INPUT_ERR


requests.delete(config.url + 'clear/v1')
    
