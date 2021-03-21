#! /usr/bin/python
# Content for create language pack

LANGUAGE = 'en_EN'
VERSION = 'v0.0.1'
AUTHOR = 'Evgeniy Yakovenko'
EMAIL = 'razor-stent@mail.ru'

""" 
MESSAGE_BOXES:
200..399 - INFORMATION
400..599 - WARNING
600..799 - CRITICAL
"""

MESSAGE_BOXES = {
    200: {'set_text': 'Found all entered tags',
          'set_title_text': 'Information',
          'set_informative_text': '',
          'set_text_detailed': ''},

    201: {'set_text': 'Uploading data successful',
          'set_title_text': 'Information',
          'set_informative_text': '',
          'set_text_detailed': ''},

    400: {'set_text': 'You have entered forbidden characters \n in tag names or the list is empty',
          'set_informative_text': "Only Latin letters are allowed, \nnumbers,,':','_' and ','",
          'set_title_text': 'Input Error',
          'set_text_detailed': ''},

    401: {'set_title_text': 'Warning',
          'set_text': 'Not all of the entered tags were found.\nCheck the spelling.',
          'set_informative_text': 'Click the "Show Details" button'
                                  '\nto view lost tags',
          'set_text_detailed': ''},

    600: {'set_text': 'An error occurred in the application',
          'set_title_text': 'Application error',
          'set_text_detailed': '',
          'set_informative_text': ''},

    601: {'set_text': 'An empty message was returned from the server',
          'set_title_text': 'Fault',
          'set_text_detailed': '',
          'set_informative_text': ''},

    602: {'set_text': 'An exception was thrown while working with the database',
          'set_text_detailed': '',
          'set_title_text': 'Error while working with the database',
          'set_informative_text': ''},

    603: {'set_text': 'The upload start date must not be \n later than the end date',
          'set_informative_text': 'Operation could not be performed',
          'set_title_text': 'Warning',
          'set_text_detailed': ''},

    604: {'set_text': 'An empty message was returned from the server',
          'set_informative_text': 'Change upload options \n (date / time)',
          'set_title_text': 'Fault',
          'set_text_detailed': ''},
}

FORM_APPLICATION = {
    'MainWindow': {'windowTitle': 'Program for downloading data from FLS ECS History server'},
    'menuFile': {'title': 'File'},
    'actionClose': {'text': 'Close'},
    'menuSettings': {'title': 'Settings'},
    'menuLanguage': {'title': 'Languages'},
    'menuHelp': {'title': 'Help'},
    'actionAbout': {'text': 'About'},
    'label_101': {'text': 'Specify the period for providing downloading'},
    'label_102': {'text': 'From'},
    'label_103': {'text': 'to'},
    'label_104': {'text': 'List of tags (separated by commas):'},
    'label_105': {'text': 'The counted number of entered tags:'},
    'label_106': {'text': 'Path to save downloading:'},
    'label_107': {'text': 'Status'},
    'label_108': {'text': 'Selecting the data output file format:'},
    'btnCheckTags': {'text': 'Check a tags in the database'},
    'btnBrowsePath': {'text': 'Folder selection'},
    'btnGetHistoryData': {'text': 'Download data'},
    'checkBox': {'text': 'Create a description file for downloaded tags'},
    'checkBox_2': {'text': 'Split data download by month (recommended)'},
    'radioButton_1_2': {'text': '*.csv (best)'}
}

STATUS = {
    0: 'Waiting',
    101: 'Running a check for tags in the database',
    102: 'A request was sent, waiting response',
    103: '',
    104: 'The answer received. Data processing 1/2',
    105: '',
    106: 'Data processing 2/2',
    107: 'Saving data to a file',
    108: 'Deleting temporary data',
    109: 'Align the width. Clearing memory ',
    110: 'Canceled',
    201: '',
    202: 'Checking the contents and sending a query',
    203: '',
    204: '',
    205: 'Canceled',
}

EVENTS = {}


