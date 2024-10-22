from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

help_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Общая информация', callback_data='about')],
    [InlineKeyboardButton(text='Обратная связь', callback_data='feedback')]])

back_help_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='help_back')]])
