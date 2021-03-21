#! /usr/bin/python
# Content for create language pack

LANGUAGE = 'ru_RU'
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
    200: {'set_text': 'Найдены все введенные теги',
          'set_title_text': 'Информация',
          'set_informative_text': '',
          'set_text_detailed': ''},

    201: {'set_text': 'Выгрузка данных прошла успешно',
          'set_title_text': 'Информация',
          'set_informative_text': '',
          'set_text_detailed': ''},

    400: {'set_text': 'Введены запрещенные символы \n в названии тегов или список пуст',
          'set_informative_text': "Разрешен ввод только латинских букв,\nцифр,':','_' и ','",
          'set_title_text': 'Ошибка ввода',
          'set_text_detailed': ''},

    401: {'set_title_text': 'Предупреждение',
          'set_text': 'Найдены не все введенные теги.\nПроверьте правильность написания.',
          'set_informative_text': 'Нажмите кнопку "Show Details" '
          '\n для просмотра не найденых тегов',
          'set_text_detailed': ''},

    600: {'set_text': 'Возникла ошибка в работе приложения',
          'set_title_text': 'Ошибка в работе приложения',
          'set_text_detailed': '',
          'set_informative_text': ''},

    601: {'set_text': 'Возвращено пустое сообщение от сервера',
          'set_title_text': "Ошибка",
          'set_text_detailed': '',
          'set_informative_text': ''},

    602: {'set_text': 'Вызвано исключение при работе с БД',
          'set_text_detailed': '',
          'set_title_text': 'Ошибка при работе с БД',
          'set_informative_text': ''},

    603: {'set_text': 'Дата начала выгрузки не должна \nбыть больше даты ее окончания',
          'set_informative_text': 'Операция не может быть выполнена',
          'set_title_text': 'Предупреждение',
          'set_text_detailed': ''},

    604: {'set_text': 'Возвращено пустое сообщение от сервера',
          'set_informative_text': 'Измените параметры выгрузки \n (дата/время)',
          'set_title_text': 'Ошибка',
          'set_text_detailed': ''},
}

FORM_APPLICATION = {
    'MainWindow': {'windowTitle': 'Программа выгрузки данных из FLS ECS History server'},
    'menuFile': {'title': 'Файл'},
    'actionClose': {'text': 'Закрыть'},
    'menuSettings': {'title': 'Настройка (Settings)'},
    'menuLanguage': {'title': 'Язык (Languages)'},
    'menuHelp': {'title': 'Помощь'},
    'actionAbout': {'text': 'О программе'},
    'label_101': {'text': 'Указать период предоставления выгрузки'},
    'label_102': {'text': 'C'},
    'label_103': {'text': 'по'},
    'label_104': {'text': 'Список тэгов (через запятую):'},
    'label_105': {'text': 'Подсчитаное количество введеных  тэгов:'},
    'label_106': {'text': 'Путь для сохранения выгрузки:'},
    'label_107': {'text': 'Состояние:'},
    'label_108': {'text': 'Выбор формата файла вывода данных:'},
    'btnCheckTags': {'text': 'Проверить наличие тегов в БД'},
    'btnBrowsePath': {'text': 'Выбор папки'},
    'btnGetHistoryData': {'text': 'Выгрузить данные'},
    'checkBox': {'text': 'Создать файл описания выгружаемых тегов'},
    'checkBox_2': {'text': 'Разделить выгрузку данных по месяцам (рекомендуется)'},
    'radioButton_1_2': {'text': '*.csv (реком.)'}
}

STATUS = {
    0: 'Ожидание',
    101: 'Запуск проверки наличия тегов в БД',
    102: 'Отправлен запрос, ожидание ответа',
    103: '',
    104: 'Ответ получен. Обработка данных 1/2',
    105: '',
    106: 'Обработка данных 2/2',
    107: 'Сохранение данных в файл',
    108: 'Удаление временных данных',
    109: 'Выравнивание ширины строк. Очистка памяти',
    110: 'Выполнено',
    201: '',
    202: 'Проверка содержимого списка и отправка запроса',
    203: '',
    204: '',
    205: 'Выполнено',
}

EVENTS = {}


