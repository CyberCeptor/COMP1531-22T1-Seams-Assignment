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
        stored_email = user["email"]
        stored_pw = user["pw"]
        if stored_email == email:
            # correct email and password
            if stored_pw == password:
                u_id = user["id"]
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
        if user["email"] == email:
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
    

    # append user data as a dictionary if everything is valid
    store['users'] = []
    user_dict = {"id": u_id, "email": email, "pw": password, 
                "first": name_first, "last": name_last, "handle": handle}
    store['users'].append(user_dict)

    return {
        'auth_user_id': u_id,
    }
