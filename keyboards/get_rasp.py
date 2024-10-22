import copy
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.time_functions import find_rasp

back_rasp_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='rasp_back')]])

back_parity_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='week_rasp')]])

get_rasp_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='На сегодня', callback_data='today_rasp'),
    InlineKeyboardButton(text='На завтра', callback_data='tomorrow_rasp')],
    [InlineKeyboardButton(text='На неделю', callback_data='week_rasp')]])

get_week_parity_kb = [
    [InlineKeyboardButton(text='1 неделя', callback_data='week_parity_1')],
    [InlineKeyboardButton(text='2 неделя', callback_data='week_parity_2')],
    [InlineKeyboardButton(text='Назад', callback_data='rasp_back')]]


def curr_week_kb():
    week_parity = find_rasp('Сегодня')[1]
    kb = copy.deepcopy(get_week_parity_kb)
    kb[week_parity][0].text = f'🗓 {kb[week_parity][0].text}'
    return InlineKeyboardMarkup(inline_keyboard=kb)
