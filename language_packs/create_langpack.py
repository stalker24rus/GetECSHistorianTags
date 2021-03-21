#! /usr/bin/python
# Script for create language pack

__author__ = 'Evgeniy Yakovenko'
__version__ = 'v.0.0.1'


# Enter path for source with LangPack Values:
from language_packs.en_EN import *
# Get function for create pickle file
from sources.func import rec_pickle_file, load_pickle_file


class LangPack:
    def __init__(self):
        self.name = LANGUAGE + '.lengpak'
        self.version = VERSION
        self.author = AUTHOR
        self.email = EMAIL
        self.events = EVENTS
        self.message_box = MESSAGE_BOXES
        self.form_app = FORM_APPLICATION
        self.status = STATUS

    def change_msg(self, number, text_name, value):
        self.message_box[number][text_name] = str(value)
        return self.message_box[number]


def main():
    """ Func for create langpack file   """
    pack = LangPack()
    rec_pickle_file(LANGUAGE + '.langpack', pack)
    load = load_pickle_file(LANGUAGE + '.langpack')
    print(dir(load))


if __name__ == '__main__':
    main()
