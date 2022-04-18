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

import time
import imgspy

import urllib

from flask import url_for #https://www.educba.com/flask-url_for/

from PIL import Image # https://pillow.readthedocs.io/en/stable/

from src.auth import check_invalid_email, check_invalid_name

from src.error import InputError
from src.token import token_valid_check, token_get_user_id
from src.other import check_valid_auth_id, cast_to_int_get_requests

from src.data_store import data_store

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
    """
        Set the users profile picture to a url of the image located in the src/static file. 
        Crops the image to the dimensions given. 

        We implement a temp folder to store and test the image being uploaded.
        Once validated, we then delete the temp image,
        open the image in the static folder to be stored for the user.
        This allows for the user to maintain their current profile picture,
        even when invalid URL's or dimensions are given.
        The image is stored as {user_id}.jpg

        Arguments:
            - token: the users token of which the profile picture is set.
            - img_url: the URL of the jpg image to be retreived and saved.
            - x_start: the start of the x axis dimension for cropping
            - y_start: the start of the y axis dimension for cropping
            - x_end: the end of the x axis dimension
            - y_end: the end of the y axis dimension
        
        Exceptions:
            - InputError:
                - the dimensions given are not integers
                - the URL given is not a string
                - the URL is not a valid address
                - the URL is not of a jpg image.
                - the dimensions given are too large for the image.

        Return Value:
            - N/A Does not return anything, sets the user data img_url.
    """

    '''Get the user ID from the token'''
    user_id = token_get_user_id(token)

    temp_image_location = f"src/temp/{user_id}.jpg"
    file_location = f"src/static/{user_id}.jpg"

    '''check that the x, y values are ints'''
    dimensions_list = [x_start, y_start, x_end, y_end]
    for item in dimensions_list:
        if type(item) is not int or item is bool:
            raise InputError("Invalid x and y value types.")

    '''Check the given URL is a string.''' 
    if type(img_url) != str:
        raise InputError("Invalid URL variable type.")

    '''Tries to open the image and saves at the temp location,'''
    try:
        urllib.request.urlretrieve(img_url, temp_image_location)
    except:
        # if not a valid URL, InputError.
        raise InputError(description="URL cannot be opened.")

    # https://github.com/nkanaev/imgspy
    """Check the URL is of a JPG."""
    image_info = imgspy.info(img_url)
    if image_info['type'] != 'jpg':
        # if the image is not jpg, raise error and delete the temp file. 
        os.remove(temp_image_location)
        raise InputError(description="URL image is not of a JPG.")

    '''Retrieve the image dimensions from the imgspy return'''
    width = image_info['width']
    height = image_info['height']

    '''Check the dimensions of the image are valid'''
    if (x_start < 0 or y_start < 0 or x_end > width or y_end > height or 
        x_start >= x_end or y_start >= y_end or x_end != y_end):
        raise InputError(description="The image cannot be uploaded with those dimensions")
    
    '''Delete the temp file, and reopen the image in the correct location'''
   # os.remove(temp_image_location)
    urllib.request.urlretrieve(img_url, file_location)
    image = Image.open(file_location)
    
    '''Crop the image to fit within our requirements'''
    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(file_location)

    # https://stackoverflow.com/questions/16351826/link-to-flask-static-files-with-url-for
    profile_img_url = url_for('static', filename=f'{user_id}.jpg', _external=True)

    store = data_store.get()

    """Locate the user in the data store, and set the img_url"""
    for users in store['users']:
        if user_id == users['id']:
            users['profile_img_url'] = profile_img_url

    data_store.set(store)

@token_valid_check
def user_stats_v1(token):
    """
    Generates user information regarding the number of channels and DM's joined,
    the number of messages sent in the channels/DM's and calculates their involvement rate.
    involvement rate:
        sum(num_channels_joined, num_dms_joined, num_msgs_sent)/sum(num_channels, num_dms, num_msgs)

    Arguments:
        - token: the users token which the stats are of.
    
    Exceptions:
        - N/A

    Return Value:
        - 'user_stats': A dictionary containing the stats generated.
    """

    store = data_store.get()
    user_id = token_get_user_id(token)
    time_stamp = int(time.time())

    channel_counter = 0
    channel_message_counter = 0
    dms_counter = 0
    dms_message_counter = 0
    total_message_counter = 0

    '''Iterates through all channels and the members if the user is a member
    Also checks the number of messages the user has sent in those channels.'''
    for channels in store['channels']:
        for members in channels['all_members']:
            if members['u_id'] == user_id:
                channel_counter += 1
                # Number of messages sent in the channel by the user
                for messages in channels['messages']:
                    if messages['u_id'] == user_id:
                        channel_message_counter += 1
                    total_message_counter += 1
                
    
    '''Iterates through all DM's and the members if the user is a member
    Also checks the number of messages the user has sent in those DM's.'''
    for dms in store['dms']:
        for members in dms['members']:
            if members['u_id'] == user_id:
                dms_counter += 1
                for messages in dms['messages']:
                    if messages['u_id'] == user_id:
                        dms_message_counter += 1
                    total_message_counter += 1


    # sum(num_channels_joined, num_dms_joined, num_msgs_sent)/sum(num_channels, num_dms, total_message_counter)
    num_channels = len(store['channels'])
    num_dms = len(store['dms'])
    num_msgs_sent = channel_message_counter + dms_message_counter

    '''If the denominator is 0, involvement should be 0. 
    If the involvement is greater than 1, it should be capped at 1.'''
    total_channel_dms_messages = (num_channels + num_dms + total_message_counter)
    if (total_channel_dms_messages <= 0):
        involvement_rate = 0.0
    else:
        involvement_rate = (channel_counter + dms_counter + num_msgs_sent) / total_channel_dms_messages
    if involvement_rate > 1:
        involvement_rate = 1.0

    # locate the user data
    for user in store['users']:
        if user['id'] == user_id:
            user_data = user

    '''Create the channels_joined dict with the information gatherd'''
    channels_joined = {
        'num_channels_joined': num_channels,
        'time_stamp': time_stamp
    }

    
    '''Create the dms_joined dict with the information gathered'''
    dms_joined = {
        'num_dms_joined': num_dms,
        'time_stamp': time_stamp}


    '''Create the messages_sent dict with the information gathered'''
    messages_sent = {
        'num_messages_sent': total_message_counter,
        'time_stamp': time_stamp
    }

    '''Append the gather information'''
    user_data['user_stats']['channels_joined'].append(channels_joined)
    user_data['user_stats']['dms_joined'].append(dms_joined)
    user_data['user_stats']['messages_sent'].append(messages_sent)
    user_data['user_stats']['involvement_rate'] = round(involvement_rate, 1)

    data_store.set(store)

    return {
        'user_stats': user_data['user_stats'],
    }


  
