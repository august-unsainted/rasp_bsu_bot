from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

reg_day_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Сегодня', callback_data='send_today')],
    [InlineKeyboardButton(text='Завтра', callback_data='send_tomorrow')]])

reg_department_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Дневное отделение', callback_data='department_full_time')],
    [InlineKeyboardButton(text='Другое', callback_data='department_other')]])
