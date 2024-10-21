from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

edit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📅 День', callback_data='edit_day'),
     InlineKeyboardButton(text='🕑 Время рассылки', callback_data='edit_time')],
    [InlineKeyboardButton(text='🎓 Группа', callback_data='edit_group'),
     InlineKeyboardButton(text='🏢 Отделение', callback_data='edit_department')],
    [InlineKeyboardButton(text='📌 Быстрая кнопка', callback_data='edit_hotkey'),
     InlineKeyboardButton(text='⚙️ Стиль отображения', callback_data='edit_settings')],
    [InlineKeyboardButton(text='⛔ Прекратить отправку сообщений', callback_data='stop')]])

edit_day_kb = [[InlineKeyboardButton(text='Сегодня', callback_data='send_today')],
               [InlineKeyboardButton(text='Завтра', callback_data='send_tomorrow')],
               [InlineKeyboardButton(text='Назад', callback_data='back')]]

edit_department_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Дневное отделение', callback_data='department_full_time')],
    [InlineKeyboardButton(text='Другое', callback_data='department_other')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]])

edit_settings_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Простое (по умолчанию)', callback_data='default_settings')],
    [InlineKeyboardButton(text='Подробное', callback_data='detailed_settings')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]])

edit_hotkey_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Расписание на сегодня', callback_data='0today_hotkey'),
    InlineKeyboardButton(text='Расписание на завтра', callback_data='1tomorrow_hotkey')],
    [InlineKeyboardButton(text='Расписание на неделю', callback_data='2full_hotkey')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]])

delete_user_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗑️ Да', callback_data='delete_user')],
    [InlineKeyboardButton(text='🙅 Нет', callback_data='dont_delete_user')]])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]])