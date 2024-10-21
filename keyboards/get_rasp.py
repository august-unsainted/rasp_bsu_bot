from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

get_rasp_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='На сегодня', callback_data='today_rasp'),
    InlineKeyboardButton(text='На завтра', callback_data='tomorrow_rasp')],
    [InlineKeyboardButton(text='На неделю', callback_data='week_rasp')]])

get_week_parity_kb = [
    InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗓 1 неделя', callback_data='week_parity_1')],
        [InlineKeyboardButton(text='2 неделя', callback_data='week_parity_2')]]),
    InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='1 неделя', callback_data='week_parity_1')],
        [InlineKeyboardButton(text='🗓 2 неделя', callback_data='week_parity_2')]])]
