from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = [ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Расписание на сегодня')],
                                         [KeyboardButton(text='Получить расписание'),
                                          KeyboardButton(text='Изменить информацию')],
                                         [KeyboardButton(text='Помощь')]],
                               resize_keyboard=True,
                               one_time_keyboard=True, input_field_placeholder='Выберите нужный пункт:'),

           ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Расписание на завтра')],
                                         [KeyboardButton(text='Получить расписание'),
                                          KeyboardButton(text='Изменить информацию')],
                                         [KeyboardButton(text='Помощь')]],
                               resize_keyboard=True,
                               one_time_keyboard=True, input_field_placeholder='Выберите нужный пункт:'),

           ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Расписание на неделю')],
                                         [KeyboardButton(text='Получить расписание'),
                                          KeyboardButton(text='Изменить информацию')],
                                         [KeyboardButton(text='Помощь')]],
                               resize_keyboard=True,
                               one_time_keyboard=True, input_field_placeholder='Выберите нужный пункт:')]
