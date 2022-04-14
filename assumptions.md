auth.py
- password can include any symbols including spaces, no checks for strength
- first and last names can include any character
- symbols from names are removed when creating handles
- the global owner is the first user to sign up to Seams
- if a user requests a reset code multiple times, only the last one will be valid
- the same randomly generated reset code can be used by a user once it has
  been used by another user and invalidated

channel.py
- channel name can contain any character
- two channels can have the same name if they have a different is_public value

token.py
- if a string containing only numbers is passed in as a token, it will be
    converted to an integer and raise an InputError rather than an AccessError
    like other strings do. This is so that integers in the query params of get
    requests will not be considered as strings

user.py
- in setname, the user's name must follow the same restrictions as when the user
    is first registered, including that their full name must have at least one char
    that is alphanumeric

dm.py
- in dm_leave, if the creator leave the dm, the creator  the creator data can 
    no longer be accessed this dm(the creator leave will make the 'creator'
    empty)

- in dm_create, the dm will have the unique dm id

- in dm_list, the user which matches the token is already in a dm

notifications.py
- users can tag themselves and they will receive a notification for it

standup.py
- standups continue even if the user who started it has left the channel/dm or
    has been removed from the channel/dm or has been removed from Seams
- standup messages cannot be empty, an input error is raised

