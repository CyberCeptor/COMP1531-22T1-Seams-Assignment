18.02
Members present: Aleesha, Yangjun (Aisha), Jenson, Xingjian (Jed)
Meeting type: Lab

25.02
Members present: Aleesha, Aisha, Jenson, Jed, Zefan
Meeting type: Lab
Assigning tasks (flexible, may double up)
auth_login: Aleesha
auth_register: Aleesha
channels_create: Jenson
channels_list: Jenson
channels_listall: Aisha
channel_join: Van
channel_invite: Van
channel_messages: Jed

Style guide (based on Aleesha's code for auth.py)
- Indentation: 4 spaces
- Variables: snake_case (same as stub code)
- Test functions: test_[feature_name]_[thing_you_are_testing]
- Comments for each test case if function name is not specific enough
- Reference any code used from internet/lectures in comments
- Add link if from internet
- 80 character margin
- Single quotation marks for strings  (‘   ’)
- Double quotation marks for docstrings (“””  “””)

03.03
Members present: Aleesha, Aisha, Jenson, Van
Meeting type: Check-in
Standup: Friday 12pm (or just anytime on Friday)
Aiming to get everything done by Saturday 10am for last autotest (push Friday evening/night latest bc pipelines gonna be slow)

Meeting notes:
- Discussion of listall_test and debug
- Discuss assumptions made(global_owner in channel_join is the first person who created the channel)
- Feedback on tests and implementations
- Debugging

04.03
Members present: Aleesha, Aisha, Jenson, Van, Jed
Meeting type: Lab
Get as much done tonight for the autotests tomorrow
Need to ask if we need a docstring at the top of each .py file and what we need to include

06.03
Members present: Aleesha, Aisha, Jenson, Van, Jed
Meeting type: check-in on teams (mainly channel_message function)
Fixing test files and implementation for channel_message

11.03
Members present: Aleesha, Aisha, Jenson, Van, Jed
Meeting type: Lab
plan:
- fix up any iteration 1 errors
- change iteration 1 tests to fit with new spec
- change iteration 1 implementation to fit new spec
- start iteration 2 implementation
aim to finish by thursday 24th! (in time for autotests then we can go back and fix)
feedback:
- extra test: check that when channel_messages is run, the return is empty
- classes for specific return types
- could be more pythonic
- branch functions into other files
- test coverage for some files good but not all
- conftest files
- more clear and descriptive commit messages
8pm Mondays meeting, standup Wednesdays, tutlab Fridays
