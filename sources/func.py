#! /usr/bin/python
# Other program function

__author__ = 'Evgeniy Yakovenko'
__version__ = 'v.0.0.1'


import pickle as pkl
import calendar
import re


def check_text(text, mask="""^[a-zA-Z0-9_:, \n\t]+$"""):
    """Check input text"""
    match = re.match(mask, text)
    return bool(match)


def get_formatted_text(text):
    """Create formatted text of list tags"""
    text = text.replace('\n', '').replace(' ', '')
    if text.endswith(','):
        text = text[:-1]
    split_text = text.split(',')
    return_text = ''
    for x in split_text:
        return_text = return_text + "'" + str(x) + "',"
    return return_text[:-1]


def rec_pickle_file(file_name, obj):
    rec_file = open(file_name, 'wb')
    pkl.dump(obj, rec_file)
    rec_file.close()
    return True


def load_pickle_file(file_name):
    load_file = open(file_name, 'rb')
    obj = pkl.load(load_file)
    load_file.close()
    return obj


def find_key(dictionary, key_word):
    """ Find key in dictionary - return str(value)"""
    if key_word in dictionary:
        return str(dictionary[key_word])
    else:
        return ''


def get_time_by_month(from_arr, to_arr):
    """
    :param from_arr:05
    :param to_arr:
    :return: ['yyyy-MM-dd hh:mm:ss, yyyy-MM-dd hh:mm:ss',...]
    """

    from_arr = from_arr.replace(' ', '-').replace(':', '-').split('-')
    to_arr = to_arr.replace(' ', '-').replace(':', '-').split('-')

    begin_date = {'year': int(from_arr[0]),
                  'month': int(from_arr[1]),
                  'day': from_arr[2],
                  'hour': from_arr[3],
                  'min': from_arr[4],
                  'sec': from_arr[5]}

    end_date = {'year': int(from_arr[0]),
                'month': int(from_arr[1]),
                'day': int(from_arr[2]),
                'hour': '23',
                'min': '59',
                'sec': '59'}

    finish_date = {'year': int(to_arr[0]),
                   'month': int(to_arr[1]),
                   'day': int(to_arr[2]),
                   'hour': to_arr[3],
                   'min': to_arr[4],
                   'sec': to_arr[5]}

    result_arr = []

    if begin_date['year'] > finish_date['year'] or \
            begin_date['year'] == finish_date['year'] and \
            begin_date['month'] > finish_date['month']:
        return None

    def set_format(number):
        if int(number) < 10:
            return '0' + str(number)
        else:
            return str(number)

    i = 0
    while True:
        # defender
        i += 1

        if begin_date['year'] < finish_date['year']:

            # set same year and month
            end_date['year'] = begin_date['year']
            end_date['month'] = begin_date['month']

            # set last day in month by year
            end_date['day'] = calendar.monthrange(begin_date['year'], begin_date['month'])[1]

            # add to arr period
            result_arr.append(str(begin_date['year']) + '-' +
                              set_format(begin_date['month']) + '-' +
                              str(begin_date['day']) + ' ' +
                              begin_date['hour'] + ':' +
                              begin_date['min'] + ':' +
                              begin_date['sec'] + ',' +
                              str(end_date['year']) + '-' +
                              set_format(end_date['month']) + '-' +
                              str(end_date['day']) + ' ' +
                              end_date['hour'] + ':' +
                              end_date['min'] + ':' +
                              end_date['sec']
                              )

            # change date for new period
            if begin_date['month'] < 12:
                begin_date['month'] += 1
            else:
                begin_date['month'] = 1
                begin_date['year'] += 1

            # reset begin date for next period
            begin_date['hour'] = '00'
            begin_date['hour'] = '00'
            begin_date['min'] = '00'
            begin_date['day'] = '01'

        else:

            if begin_date['month'] == finish_date['month']:
                result_arr.append(str(begin_date['year']) + '-' +
                                  set_format(begin_date['month']) + '-' +
                                  str(begin_date['day']) + ' ' +
                                  begin_date['hour'] + ':' +
                                  begin_date['min'] + ':' +
                                  begin_date['sec'] + ',' +
                                  str(finish_date['year']) + '-' +
                                  set_format(finish_date['month']) + '-' +
                                  str(finish_date['day']) + ' ' +
                                  finish_date['hour'] + ':' +
                                  finish_date['min'] + ':' +
                                  finish_date['sec']
                                  )
                break

            if begin_date['month'] <= finish_date['month']:

                # mask ['yyyy - MM - dd - hh - mm - ss, yyyy - MM - dd - hh - mm - ss',...])
                # set same year and month
                end_date['year'] = begin_date['year']
                end_date['month'] = begin_date['month']

                # set last day in month by year
                end_date['day'] = calendar.monthrange(begin_date['year'], begin_date['month'])[1]

                # add to arr period
                result_arr.append(str(begin_date['year']) + '-' +
                                  set_format(begin_date['month']) + '-' +
                                  str(begin_date['day']) + ' ' +
                                  begin_date['hour'] + ':' +
                                  begin_date['min'] + ':' +
                                  begin_date['sec'] + ',' +
                                  str(end_date['year']) + '-' +
                                  set_format(end_date['month']) + '-' +
                                  str(end_date['day']) + ' ' +
                                  end_date['hour'] + ':' +
                                  end_date['min'] + ':' +
                                  end_date['sec']
                                  )

                # change date for new period
                if begin_date['month'] < 12:
                    begin_date['month'] += 1

                # reset begin date for next period
                begin_date['hour'] = '00'
                begin_date['hour'] = '00'
                begin_date['min'] = '00'
                begin_date['day'] = '01'

        if i > 10000:
            break
    return result_arr


