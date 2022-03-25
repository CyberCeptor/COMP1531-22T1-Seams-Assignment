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

14.03
Members present: Aleesha, Aisha, Jenson, Van, Jed
Meeting type: check-in
to get done by Friday this week:
- change tests to work with GET, POST requests for v2 of our functions
next step:
- start implementation on v2 functions

18.03
Members present: Aleesha, Aisha, Jenson, Van, Jed
Meeting type: Lab
- complete at least v2 functions by Tuesday for first autotests
- push regularly
- create new http functions in server.py for now and we can separate later if needed
- keeping Monday 8pm meeting, Wednesday standup, Friday meeting schedule unless we want more during flexi week

21.03
Members present: Aleesha, Aisha, Jenson, Van
Meeting type: check-in
- complete v2 pytests and implementations by tomorrow night

25.03
Members present: Aleesha, Aisha, Van, Jed
Meeting type: check-in
- completing all functions implementation by tonight for autotest tomorrow

for style (over the weekend):
- implementation functions follow the docstring format of description, arguments, exceptions, return value
- modules(files) follow docstring format of filename, author, created, description
- pytests functions can just have one description at the top with comments throughout if theres a lot of tests
- error messages should have description= in front of it 



