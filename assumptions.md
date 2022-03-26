auth.py
- password can include any symbols including spaces, no checks for strength
- first and last names can include any character
- symbols from names are removed when creating handles
- the global owner is the first user to sign up to Seams

channels.py
- channel name can contain any character
- two channels can have the same name if they have a different is_public value

tokens.py
- if a string containing only numbers is passed in as a token, it will be
    converted to an integer and raise an InputError rather than an AccessError
    like other strings do. This is so that integers in the query params of get
    requests will not be considered as strings

user.py
- in setname, the user's name must follow the same restrictions as when the user
    is first registered, including that their full name must have at least one char
    that is alphanumeric
