# pylint: disable=raise-missing-from
"""
Filename: user.py

Author: Jenson Morgan(z5360181), Xingjian Dong (z5221888)
Created: 22/02/2022 - 28/03/2022

Description:
    user.py contains the implementation for
    -   user_profile_v1: return the user information from a token and u_id.
    -   user_setemail_v1: set a new email for the user, in users, and the
        channels the user is in
    -   user_setname_v1: set the user's first name and last name, in the user
        and channels data_store
    - user_set_handle_v1: set the user's handle with the new information
        Helper Function: 
            - check_valid_handle: checks the handle is authentic
"""

from src.data_store import data_store
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id, cast_to_int_get_requests
from src.auth import check_invalid_email, check_invalid_name
from src.error import InputError
from PIL import Image # https://pillow.readthedocs.io/en/stable/
import urllib
from flask import url_for #https://www.educba.com/flask-url_for/
import requests
import imgspy
import os

@token_valid_check
def user_profile_v1(token, u_id):
    """
    For a valid user, returns information about their user_id, firstname,
    last name, and handle

    Arguments:
        token (str) - a valid jwt token string
        u_id (int)  - an int specifying a user

    Exceptions: N/A

    Return: Returns a user's user_id, email, name_first, name_last, handle_str
    """

    # cast u_id into an int since it is a GET request
    u_id = cast_to_int_get_requests(u_id, 'user id')

    # grab the user data after checking if the u_id is valid
    user = check_valid_auth_id(u_id)

    return {
        'user': user['return_data']
    }

@token_valid_check
def user_profile_setemail_v1(token, email):
    """
    Update the authorised user's email
    
    Arguments:
        -   token
        -   email
    
    Exceptions:
        InputError: given email does not match the given valid email regex
    
    Return Value: N/A
    """

    store = data_store.get()

    # check the email is valid (i.e. usable email address, format)
    # check that the email isn't already used by another user
    # both done by check_invalid_email.

    user_id = token_get_user_id(token)

    check_invalid_email(store, str(email))

    # set the user email to the new email
    for user in store['users']:
        if user['id'] == user_id:
            user['email'] = email

    # iterate through all channels that the member is in and set 
    # the email there aswell.

    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['email'] = email
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['email'] = email

    for dm in store['dms']:
        for user in dm['members']:
            if user['u_id'] == user_id:
                user['email'] = email

    data_store.set(store)

@token_valid_check
def user_profile_setname_v1(token, name_first, name_last):
    """
    Update the authorised user's first and last name
    
    Arguments:
        -   token
        -   name_first
        -   name_last
    
    Exceptions:
        InputError:
            -  length of name_first is not between 1 and 50 characters inclusive
            -  length of name_last is not between 1 and 50 characters inclusive
    
    Return Value: N/A
    """

    store = data_store.get()

    # check the name is valid (i.e. usable name_first, name_last)
    # both done by check_invalid_name.
    # need to check that the name is the correct format.

    user_id = token_get_user_id(token)

    if type(name_first) is not str or type(name_first) is bool:
        raise InputError(description='Invalid first name')

    if type(name_last) is not str or type(name_last) is bool:
        raise InputError(description='Invalid last name')

    check_invalid_name(name_first, name_last)

    # set the user name to the new name
    for user in store['users']:
        if user['id'] == user_id:
            user['first'] = name_first
            user['last'] = name_last

    # iterate through all channels that the member is in and set 
    # the name there aswell.

    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['name_first'] = name_first
                user['name_last'] = name_last
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['name_first'] = name_first
                user['name_last'] = name_last

    for dm in store['dms']:
        for user in dm['members']:
            if user['u_id'] == user_id:
                user['name_first'] = name_first
                user['name_last'] = name_last

    data_store.set(store)

def check_invalid_handle(store, handle_str):
    """
    checks if a given handle_str is invalid

    Arguments:
        store (data)     - the stored data
        handle_str (str) - a str that the user wants to change their handle to

    Exceptions: 
        InputError - Raised if handle_str input is of invalid type, length, is 
                     not alphanumeric, and if a user already has the same handle

    Return Value: N/A
    """

    # check handle is string or bool
    if type(handle_str) is not str or type(handle_str) is bool:
        raise InputError(description='Invalid handle_str')

    # check for invalid handle_str
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description='Invalid handle_str')
    
    # check for invalid handle_str
    if handle_str.isalnum() is False:
        raise InputError(description='Invalid handle_str')

    # check for duplicate handle_str
    for user in store['users']:
        if user['handle'] == handle_str and user['removed'] is False:
            raise InputError(description='Handle has already been taken')

@token_valid_check
def user_profile_sethandle_v1(token, handle_str):
    """
    updates a user's handle to the given handle_str if valid

    Arguments:
        token (str)      - a valid jwt token string
        handle_str (str) - a str that the user wants to change their handle to

    Exceptions: 
        InputError - Raised if handle_str input is invalid

    Return Value: N/A
    """

    store = data_store.get()

    user_id = token_get_user_id(token)

    check_invalid_handle(store, handle_str)

    # set user's handle to new handle in stored data
    for user in store['users']:
        if user['id'] == user_id:
            user['handle'] = handle_str

    # set user's handle to new handle in channel data
    for channel in store['channels']:
        for user in channel['all_members']:
            if user['u_id'] == user_id:
                user['handle_str'] = handle_str
        for user in channel['owner_members']:
            if user['u_id'] == user_id:
                user['handle_str'] = handle_str

    # set user's handle to new handle in dm data
    for dm in store['dms']:
        for user in dm['members']:
            if user['u_id'] == user_id:
                user['handle_str'] = handle_str

    data_store.set(store)

@token_valid_check
def user_profile_uploadphoto_v1(token, img_url, x_start, y_start, x_end, y_end):
    '''Check the token is valid'''

    """
    urlretrieve:
        - url: the url to GET the JPG
        - filename: specifies the local path (if not specified, urllib will generate a temporary file to save the data)
        - reporthook: callback function, which will trigger when the server is connected and the corresponding 
        data block is transferred. We can use this callback function to display the current download progress.
        - data (data of the POST import server): returns a tuple containing two elements (filename, headers). Filename
        represents the path saved to the local, and header represents the reponse header of the server.
    """

    '''check that the x, y values are ints'''
    dimensions_list = [x_start, y_start, x_end, y_end]
    for item in dimensions_list:
        if type(item) is not int or item is bool:
            raise InputError("Invalid x and y value types.")
    
    '''Get the user ID from the token'''
    user_id = token_get_user_id(token)

    file_location = f"uploads/{user_id}.jpg"
    temp = f"uploads/temp.jpg"
    
    # # https://stackoverflow.com/questions/64384834/how-to-check-file-type-for-an-image-stored-as-url
    # response = requests.get(img_url)
    # if response.headers['Content-Type'] != 'image/jpeg':
    #     raise InputError(description="URL image is not of a JPG.")    


    if type(img_url) != str:
        raise InputError("Invalid URL variable type.")

    '''Test the URL can be opened
    Stores in temp file, incase its not valid.'''
    try:
        urllib.request.urlretrieve(img_url, temp)
    except:
        raise InputError(description="URL cannot be opened.")


    
    # https://github.com/nkanaev/imgspy
    """Check the URL is of a JPG."""
    image_info = imgspy.info(img_url)
    if image_info['type'] != 'jpg':
        os.remove(temp)
        raise InputError(description="URL image is not of a JPG.")



    

    image = Image.open(temp)

    width = image_info['width']
    height = image_info['height']


    '''Check the dimensions of the image'''
    if x_start < 0 or y_start < 0 or x_end > width or y_end > height or x_start >= x_end or y_start >= y_end or x_end != y_end:
        os.remove(temp)
        raise InputError(description="The image dimensions are too small.")
    
    '''Crop the image to fit within our requirements'''
    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(file_location)

    # https://stackoverflow.com/questions/16351826/link-to-flask-static-files-with-url-for
    profile_img_url = url_for('static', filename=f'uploads/{user_id}.jpg')

    
    """Set the user data profile_img_url to be the URL image"""
    store = data_store.get()
    user_data = check_valid_auth_id(user_id)
    user_data['profile_img_url'] = profile_img_url
    data_store.set(store)
    return {}
