#! /usr/bin/python
# Start Main Application

__author__ = 'Evgeniy Yakovenko'
__version__ = 'v.0.2.2'

import sys
import openpyxl
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from datetime import datetime
import ui.mainform as design
from sources.sql import EcsHistorianDriver as SqlClass
from sources.func import rec_pickle_file, load_pickle_file, find_key, get_time_by_month


DB = SqlClass()


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):

        # program values
        self.lpk = LangPack()
        self.db = SqlClass()
        self.tags_list = ()
        self.using_language = 'ru_RU'  # or 'en_EN'
        self.time_cu = 0
        self.parts = ''
        self.output_file_type = 1
        super().__init__()

        # set events and window options
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setupUi(self)
        self.setCentralWidget(self.centralwidget)
        self.btnBrowsePath.clicked.connect(self.browse_folder)
        self.btnGetHistoryData.clicked.connect(self.run_get_history_value_task)
        self.pteTagList.textChanged.connect(self.score_tags)
        self.btnCheckTags.clicked.connect(self.run_get_valid_tags_task)
        self.actionEnglish.triggered.connect(lambda: self.change_language('en_EN'))
        self.actionRussian.triggered.connect(lambda: self.change_language('ru_RU'))
        self.actionAbout.triggered.connect(self.about)
        self.actionClose.triggered.connect(self.close_app)
        self.checkBox_2.setChecked(True)
        self.radioButton_1_1.toggled.connect(self.set_output_file)
        self.radioButton_1_2.toggled.connect(self.set_output_file)
        self.radioButton_1_2.setChecked(True)
        self.ptePathToSave.setReadOnly(True)
        self.setAcceptDrops(True)

        # prepare form
        self.get_data_form()
        self.change_language(self.using_language)
        self.set_work_status(0)
        self.set_progress_bar(0)

        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.count_up)

    def set_output_file(self):
        if self.radioButton_1_1.isChecked():
            self.output_file_type = 0

        if self.radioButton_1_2.isChecked():
            self.output_file_type = 1

    def browse_folder(self):
        """ Choice path for save the file """
        try:
            directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
            if directory:
                self.ptePathToSave.setPlainText(directory)
        except BaseException as e:
            self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))

    def score_tags(self):
        """ Score number input tags """
        try:
            text = self.pteTagList.toPlainText()
            if text == '':
                self.out_num_tags.setText('0')
            else:
                if text.endswith(','):
                    text = text[:-1]
                text = text.split(',')
                self.out_num_tags.setText(str(len(text)))
        except BaseException as e:
            self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))

    def count_up(self):
        """ Count past time for running subprocess """
        self.time_cu += 1
        self.timer_up.setText(str(self.time_cu) + ' s')

    def start_cu(self):
        """Run timer for count_up"""
        self.timer.start(1000)

    def stop_cu(self):
        """Stop timer for count_up"""
        self.timer.stop()

    def reset_cu(self):
        """Reset counter of past time"""
        self.time_cu = 0
        self.timer_up.setText('0 s')

    def show_langpack_msg_box(self, code, set_text_detailed=''):
        """ Translate message code to text message by using language """
        msg_dict = self.lpk.message_box[code]
        icon = QtWidgets.QMessageBox.Information
        if 200 < code <= 399:
            icon = QtWidgets.QMessageBox.Information

        if 400 < code <= 599:
            icon = QtWidgets.QMessageBox.Warning

        if 600 < code <= 799:
            icon = QtWidgets.QMessageBox.Critical

        if set_text_detailed == '':
            set_text_detailed = msg_dict['set_text_detailed']

        show_msg_box(set_qt_icon=icon,
                     set_title_text=msg_dict['set_title_text'],
                     set_text=msg_dict['set_text'],
                     set_informative_text=msg_dict['set_informative_text'],
                     set_text_detailed=set_text_detailed)

    def change_language(self, lang):
        """ Change languages between en_EN and ru_RU """

        # Russian
        if lang == 'ru_RU':
            self.actionRussian.setChecked(True)
            self.actionEnglish.setChecked(False)
            self.using_language = lang

        # English
        if lang == 'en_EN':
            self.actionEnglish.setChecked(True)
            self.actionRussian.setChecked(False)
            self.using_language = lang

        # Check argument
        if lang in ('ru_RU', 'en_EN'):
            try:
                # Get language pack from file
                file_name = 'language_packs\\' + lang + '.langpack'
                self.lpk = load_pickle_file(file_name)
                form_app = self.lpk.form_app

                # Search object for replace text values
                for key in form_app:
                    if key == 'MainWindow':
                        self.setWindowTitle(form_app[key]['windowTitle'])

                    # Object filters
                    for obj in (self.findChild(QtWidgets.QLabel, key),
                                self.findChild(QtWidgets.QAction, key),
                                self.findChild(QtWidgets.QPushButton, key),
                                self.findChild(QtWidgets.QMainWindow, key),
                                self.findChild(QtWidgets.QMenu, key),
                                self.findChild(QtWidgets.QCheckBox, key),
                                self.findChild(QtWidgets.QRadioButton, key)):

                        # Find something and set text on language
                        if obj is not None:

                            if isinstance(obj, QtWidgets.QLabel) \
                                    or isinstance(obj, QtWidgets.QAction) \
                                    or isinstance(obj, QtWidgets.QPushButton) \
                                    or isinstance(obj, QtWidgets.QCheckBox)\
                                    or isinstance(obj, QtWidgets.QRadioButton):
                                obj.setText(form_app[key]['text'])

                            if isinstance(obj, QtWidgets.QMainWindow):
                                self.setWindowTitle(form_app[key]['windowTitle'])

                            if isinstance(obj, QtWidgets.QMenu):
                                obj.setTitle(form_app[key]['title'])

                self.set_work_status(0)
            except Exception as e:
                self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))

    def get_data_form(self):
        """ Get data from file to dataform """
        try:
            data = load_pickle_file('data_form.pickle')
            self.pteTagList.setPlainText(data['list_of_tags'])
            self.dteTimeFrom.setDateTime(data['date_time_from'])
            self.dteTimeTo.setDateTime(data['date_time_to'])
            self.ptePathToSave.setPlainText(data['path_folder'])
            self.using_language = data['using_language']
            self.change_language(self.using_language)
            return True
        except Exception as e:
            self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))
            return False

    def save_data_form(self):
        """ Save dataform to file"""
        try:
            data = {'list_of_tags': self.pteTagList.toPlainText(),
                    'date_time_from': self.dteTimeFrom.dateTime(),
                    'date_time_to': self.dteTimeTo.dateTime(),
                    'path_folder': self.ptePathToSave.toPlainText(),
                    'using_language': self.using_language}
            rec_pickle_file('data_form.pickle', data)
            return True
        except Exception as e:
            self.show_langpack_msg_box(603, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', '')[1:-1])
            return False

    def check_date_time_input(self):
        """Function for compare input tags list with tags in ECS DB Historian"""
        if self.dteTimeFrom.dateTime() > self.dteTimeTo.dateTime():
            self.show_langpack_msg_box(603)
            return False
        else:
            return True

    def set_work_status(self, step=0):
        """Set work status by step"""
        case = self.lpk.status
        self.program_state.setText(self.parts + ' ' + case[step])
        return step

    def set_progress_bar(self, step=0):
        """Set progress bar value by step"""
        case = {
            0: 0, 10: 10, 20: 20, 30: 30, 40: 40, 50: 50, 60: 60, 70: 70, 80: 80, 90: 90, 100: 100,
            101: 10, 102: 20, 103: 30, 104: 40, 105: 50, 106: 60, 107: 70, 108: 80, 109: 90, 110: 100,
            201: 20, 202: 40, 203: 60, 204: 80, 205: 100
        }
        self.progressBar.setValue(case[step])
        return step

    def set_status(self, msg):
        """ Set value to progress bar """
        if msg is not None:
            if isinstance(msg, dict):
                if 'progress_code' in msg:
                    self.set_progress_bar(self.set_work_status(msg['progress_code']))

    def show_msg(self, msg):
        if isinstance(msg, dict):
            if 'message_code' in msg:
                self.show_langpack_msg_box(msg['message_code'],
                                           set_text_detailed=find_key(msg, 'set_text_detailed'))

    def set_parts(self, msg):
        if isinstance(msg, dict):
            if 'progress_part' in msg:
                self.parts = msg['progress_part']

    def run_get_valid_tags_task(self):
        """ Run task for validation a tags in ECS Historian DB """
        try:
            self.start_cu()
            # Create a QThread object
            self.thread = QThread()

            # Create a worker object
            self.worker = Worker(tags_list=self.pteTagList.toPlainText())

            # Move worker to the thread
            self.worker.moveToThread(self.thread)

            # Connect signals and slots
            self.thread.started.connect(self.worker.run_get_valid_tags)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            self.worker.send_progress_code.connect(self.set_status)
            self.worker.send_message.connect(self.show_msg)
            self.worker.start_timer.connect(self.start_cu)
            self.worker.stop_timer.connect(self.stop_cu)
            self.worker.reset_timer.connect(self.reset_cu)

            # Start the thread
            self.thread.start()

            # Final resets
            self.disable_buttons()

            self.thread.finished.connect(
                lambda: self.finish_tread_options(deselect_checkbox=False)
            )

        except Exception as e:
            self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))

    def run_get_history_value_task(self):
        """ Run task for getting a table with historian value of tags """
        try:
            # Create a QThread object
            self.thread = QThread()

            # Create a worker object
            self.worker = Worker(tags_list=self.pteTagList.toPlainText(),
                                 create_desc_file=self.checkBox,
                                 path=self.ptePathToSave,
                                 time_from=self.dteTimeFrom,
                                 time_to=self.dteTimeTo,
                                 output_file_type=self.output_file_type,
                                 out_by_month=self.checkBox_2.isChecked())

            # Move worker to the thread
            self.worker.moveToThread(self.thread)

            # Connect signals and slots

            self.thread.started.connect(self.worker.run_get_value)

            '''if self.checkBox_2.isChecked():
                self.thread.started.connect(self.worker.run_get_value)
            else:
                self.thread.started.connect(self.worker.run_get_history_value)'''

            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.send_progress_code.connect(self.set_status)
            self.worker.send_progress_part.connect(self.set_parts)
            self.worker.send_message.connect(self.show_msg)
            self.worker.start_timer.connect(self.start_cu)
            self.worker.stop_timer.connect(self.stop_cu)
            self.worker.reset_timer.connect(self.reset_cu)

            # Start the thread
            self.thread.start()

            # Final resets
            self.disable_buttons()
            self.thread.finished.connect(
                lambda: self.finish_tread_options()
            )

        except Exception as e:
            self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))

    def disable_buttons(self):
        self.btnGetHistoryData.setEnabled(False)
        self.btnCheckTags.setEnabled(False)

    def finish_tread_options(self, deselect_checkbox=True):
        self.btnGetHistoryData.setEnabled(True)
        self.btnCheckTags.setEnabled(True)
        self.parts = ''
        if deselect_checkbox:
            self.checkBox.setChecked(False)
        self.reset_cu()

    def close_app(self):
        """ Closing procedure by button """
        try:
            self.save_data_form()
            self.close()
        except Exception as e:
            self.show_langpack_msg_box(600, set_text_detailed=str(e).replace('\\n', '\\\n').replace('\\', ''))

    def closeEvent(self, event):
        """ Save dataform when exit application """
        self.save_data_form()

    def about(self):
        """ Show about dialog """
        if self.using_language == 'ru_RU':
            show_msg_box(set_qt_icon=QtWidgets.QMessageBox.Information,
                         set_title_text='GetHistTags ' + __version__,
                         set_text='Программа для выгрузки истории тегов из БД FLS ECS Historian \n\n' +
                                  'Лицензия LGPL\n' +
                                  'E-mail: razor-stent@mail.ru\n\n' +
                                  'Работает на программном обеспечении с открытым исходным кодом\n\n' +
                                  'Copyright 2021 (c) Яковенко Е.Г.'
                         )

        if self.using_language == 'en_EN':
            show_msg_box(set_qt_icon=QtWidgets.QMessageBox.Information,
                         set_title_text='GetHistTags ' + __version__,
                         set_text='Program for download historian tags from FLS ECS Historian \n\n' +
                                  'License LGPL\n' +
                                  'E-mail: razor-stent@mail.ru\n\n' +
                                  'Powered by open-sourse-software \n\n' +
                                  'Copyright 2021 (c) Yakovenko E.G.'
                         )


class Worker(QObject):
    finished = pyqtSignal()
    send_progress_code = pyqtSignal(dict)
    send_progress_part = pyqtSignal(dict)
    send_message = pyqtSignal(dict)
    result_out = pyqtSignal(dict)
    start_timer = pyqtSignal()
    stop_timer = pyqtSignal()
    reset_timer = pyqtSignal()
    show_complete_msg = False

    def __init__(self, **kwargs):

        super().__init__()

        self.out_by_month = True

        # Check and set arguments
        for key, value in kwargs.items():

            if key == 'tags_list':
                self.tags_list = value

            if key == 'show_complete_msg':
                self.show_complete_msg = value

            if key == 'create_desc_file':
                """QCheckBox - obj"""
                self.create_desc_file = value

            if key == 'path':
                """QPlainTextEdit - obj"""
                self.path = value

            if key == 'time_from':
                """QDateTimeEdit - obj"""
                self.time_from = value

            if key == 'time_to':
                """QDateTimeEdit - obj"""
                self.time_to = value

            if key == 'output_file_type':
                self.output_file_type = value

            if key == 'out_by_month':
                self.out_by_month = value

    def run_get_valid_tags(self):
        """Running method for validation a tags in ECS Historian DB"""
        try:

            if isinstance(self.show_complete_msg, bool):
                self.start_timer.emit()

                self.__get_valid_tags()

                self.stop_timer.emit()
                self.finished.emit()
                return True
            else:
                return False
        except Exception as e:
            print(str(e).replace('\\n', '\\\n').replace('\\', ''))

    def run_get_value(self):
        """ Running method for getting a table with historian value of tags """
        try:
            if isinstance(self.create_desc_file, QtWidgets.QCheckBox) \
                    and isinstance(self.path, QtWidgets.QPlainTextEdit) \
                    and isinstance(self.time_from, QtWidgets.QDateTimeEdit) \
                    and isinstance(self.time_to, QtWidgets.QDateTimeEdit):

                now = datetime.now()
                file_name_prefix = now.strftime("%d_%m_%Y_%H_%M_%S_%f")

                # run timer
                self.start_timer.emit()

                # get tags list
                returned_tags_list = self.__get_valid_tags(show_msg=False)

                # run timer past execution self.__get_valid_tags
                self.start_timer.emit()

                # get description file if selected
                if self.create_desc_file.isChecked():
                    self.__get_description_file()

                process_result = False

                if self.__check_date_time_input():
                    if self.out_by_month:
                        # get list of datetime  separately by month
                        list_datetime = get_time_by_month(self.time_from.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
                                                          self.time_to.dateTime().toString("yyyy-MM-dd hh:mm:ss"))

                        # number_download_parts = len(list_datetime)
                        if list_datetime is not None:
                            for i in range(len(list_datetime)):
                                self.send_progress_part.emit({'progress_part': '[' + str(i + 1) + '/' +
                                                                               str(len(list_datetime)) + ']'
                                                              })

                                # processing data
                                process_result = self.__get_value(returned_tags_list,
                                                                  list_datetime[i].split(',')[0],
                                                                  list_datetime[i].split(',')[1],
                                                                  file_name_prefix)

                                if False is process_result:
                                    # Show message about blank data from server
                                    self.send_message.emit({'message_code': 604})
                                    self.send_progress_code.emit({'progress_code': 0})
                                    break
                    else:
                        # by one period
                        self.send_progress_part.emit({'progress_part': '[1/1]'})
                        process_result = self.__get_value(returned_tags_list,
                                                          self.time_from.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
                                                          self.time_to.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
                                                          file_name_prefix)
                        if False is process_result:
                            # Show message about blank data from server
                            self.send_message.emit({'message_code': 604})
                            self.send_progress_code.emit({'progress_code': 0})

                self.send_progress_part.emit({'progress_part': ''})
                self.send_progress_code.emit({'progress_code': 0})
                if True is process_result:
                    self.send_message.emit({'message_code': 201})

                self.stop_timer.emit()
                self.finished.emit()

        except Exception as e:
            # Show message about exception
            self.send_message.emit({'message_code': 600,
                                    'set_text_detailed': str(e).replace('\\n', '\\\n').replace('\\', '')})
            self.send_progress_part.emit({'progress_part': ''})
            self.send_progress_code.emit({'progress_code': 0})
            self.stop_timer.emit()
            self.finished.emit()

    def __get_valid_tags(self, show_msg=True):
        """ Inner method for validation a tags in ECS Historian DB"""
        try:
            self.send_progress_code.emit({'progress_code': 202})
            result_db = DB.get_compared_dict(self.tags_list)
            self.send_progress_code.emit({'progress_code': 205})
            if result_db is not None:
                if len(result_db) > 0:
                    if result_db is not None and result_db['bad_list_tags'] != '':
                        self.result_out.emit(result_db)
                        self.send_message.emit({'message_code': 401,
                                                'set_text_detailed': result_db['bad_list_tags']})
                        self.send_progress_code.emit({'progress_code': 0})
                        self.stop_timer.emit()
                        self.finished.emit()
                        return result_db
                    else:
                        if show_msg:
                            self.send_message.emit({'message_code': 200})
                        self.result_out.emit(result_db)
                        self.send_progress_code.emit({'progress_code': 0})
                        self.stop_timer.emit()
                        return result_db
                else:
                    self.send_message.emit({'message_code': 601})
                    self.send_progress_code.emit({'progress_code': 0})
            else:
                self.send_message.emit({'message_code': 400})
                self.send_progress_code.emit({'progress_code': 0})
            self.stop_timer.emit()
            return None

        except Exception as e:
            self.send_message.emit({'message_code': 602,
                                    'set_text_detailed': str(e).replace('\\n', '\\\n').replace('\\', '')})
            self.send_progress_code.emit({'progress_code': 0})
            self.stop_timer.emit()
            return None

    def __get_value(self, returned_tags_list, data_from, data_to, file_name_prefix):
        """ Inner method for getting a table with historian value of tags """
        # Send progress
        self.send_progress_code.emit({'progress_code': 101})

        # Checking inputs parameter
        if returned_tags_list is not None \
                and len(returned_tags_list) > 0 \
                and returned_tags_list['good_list_tags'] != '' \
                and self.__check_date_time_input():

            self.send_progress_code.emit({'progress_code': 102})

            # Get data from server
            result = DB.get_tags_hist_value(returned_tags_list['good_list_tags'],
                                            data_from,
                                            data_to)

            if len(result) > 0:
                #  Set columns name for DataFrame
                cols = ['DateTime', 'TagName', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
                        43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]

                # Transforming data
                # Part 1/2
                self.send_progress_code.emit({'progress_code': 104})

                df = pd.DataFrame(result, columns=cols)

                del result

                df1 = df.melt(['DateTime', 'TagName'], var_name='minutes', value_name='data')

                del df  # Clear memory

                df1['DateTime'] += pd.to_timedelta(df1['minutes'], unit='Min')

                # Part 2/2
                self.send_progress_code.emit({'progress_code': 106})
                df2 = df1.pivot('DateTime', 'TagName', 'data')

                del df1  # Clear memory

                file_extantion = '.csv'

                if self.output_file_type == 0:
                    file_extantion = '.xlsx'

                if self.output_file_type == 1:
                    file_extantion = '.csv'

                # Create file name
                if self.path.toPlainText() == '':
                    file_name = str(data_from.replace(':', '_').replace(' ', '_') + '_' +
                                    data_to.replace(':', '_').replace(' ', '_') + '_' +
                                    file_name_prefix + file_extantion
                                    )
                else:
                    file_name = str(self.path.toPlainText() + '\\' +
                                    data_from.replace(':', '_').replace(' ', '_') + '_' +
                                    data_to.replace(':', '_').replace(' ', '_') + '_' +
                                    file_name_prefix + file_extantion
                                    )

                # Save DataFrame to xlsx file
                self.send_progress_code.emit({'progress_code': 107})

                # Save to file
                if self.output_file_type == 0:
                    df2.to_excel(file_name, startrow=0)
                if self.output_file_type == 1:
                    df2.to_csv(file_name)

                self.send_progress_code.emit({'progress_code': 108})

                # Clear memory
                del df2

                self.send_progress_code.emit({'progress_code': 109})
                self.send_progress_code.emit({'progress_code': 110})
                self.send_progress_code.emit({'progress_code': 0})
                return True
            else:
                return False

    def __check_date_time_input(self):
        """ Function for compare input tags list with tags in ECS DB Historian """
        if self.time_from.dateTime() >= self.time_to.dateTime():
            self.send_message.emit({'message_code': 603})
            return False
        else:
            return True

    def __get_description_file(self):
        now = datetime.now()
        file_name_prefix = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
        # Run timer past execution self.__get_valid_tags
        self.start_timer.emit()

        # Get description file
        if self.create_desc_file.isChecked():

            # Create description file of tags
            if self.path.toPlainText() == '':
                file_name = str('description_' + file_name_prefix + '.xlsx')
            else:
                file_name = str(self.path.toPlainText() + '\\' + 'description_' + file_name_prefix + '.xlsx')
            save_description_file(self.tags_list, file_name)
            set_max_col_width_xl(file_name)


class LangPack:
    """ Language data type """
    name = ''
    version = ''
    author = ''
    email = ''
    events = {}
    message_box = {}
    form_app = {}
    status = {}

    def change_msg(self, number, text_name, value):
        """ Add or Change message dictionary """
        self.message_box[number][text_name] = str(value)
        return self.message_box[number]


def save_description_file(tag_list, file_name='Description'):
    """ Create file of descriptions by tag list """
    df = pd.DataFrame(DB.get_tags_list(tag_list))
    df.to_excel(file_name, startrow=0, header=False, index=False)
    del df


def set_max_col_width_xl(file):
    """ Set max align width for xls file """
    wb = openpyxl.load_workbook(file)
    sheet = wb.active

    for col in sheet.columns:
        max_length = 0
        column = col[0].column_letter  # Get the column name

        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except Exception:
                pass

        adjusted_width = (max_length + 2 * 1.2)
        sheet.column_dimensions[column].width = adjusted_width
    wb.save(file)
    del wb


def show_msg_box(**kwargs):
    """Show message box form"""
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)

    for key, value in kwargs.items():

        if key == 'set_qt_icon':
            msg.setIcon(value)

        if key == 'set_text':
            msg.setText(value)

        if key == 'set_informative_text':
            msg.setInformativeText(value)

        if key == 'set_title_text':
            msg.setWindowTitle(value)

        if key == 'set_text_detailed':
            msg.setDetailedText(value)
    msg.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
    # pyuic5 mainform.ui -o mainform.py
    # from program_components.QtFormsPath.mycustomplaintext import MyCustomPlainText
