import re

from src.data_store import data_store
from src.error import InputError

valid_email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
# based on examples written by others https://stackoverflow.com/questions/
# 2385701/regular-expression-for-first-and-last-name
valid_name_regex = r'^[a-zA-Z\'\-\s]{1,50}$'

def auth_login_v1(email, password):
    store = data_store.get()
    u_id = -1
    for user in store['users']:
        if user[1] == email:
            # correct email and password
            if user[2] == password:
                u_id = user[0]
            else: # email belongs to a user but incorrect password
                raise InputError("Incorrect password")

    # if u_id = -1 then a user with given email does not exist
    if u_id == -1:
        raise InputError("Email does not belong to a user")

    return {
        'auth_user_id': u_id,
    }

# based on code Haydon wrote in project starter video
def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()
    u_id = len(store['users']) + 1

    # check for valid email address
    if not re.fullmatch(valid_email_regex, email):
        raise InputError("Invalid email address")

    # check for duplicate email
    for user in store['users']:
        if user[1] == email:
            raise InputError("Email has already been taken")

    # check for invalid password
    if len(password) < 6:
        raise InputError("Password is too short")
    elif ' ' in password:
        raise InputError("Password contains a space")

    # check for invalid first name
    if not re.fullmatch(valid_name_regex, name_first):
        raise InputError("Invalid first name")
    
    # check for invalid last name
    if not re.fullmatch(valid_name_regex, name_last):
        raise InputError("Invalid last name")

    # create a handle
    

    # append user data if everything is valid
    store['users'] = []
    store['users'].append((u_id, email, password, name_first, name_last))

    return {
        'auth_user_id': u_id,
    }
