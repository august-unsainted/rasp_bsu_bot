import copy
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from utils.db_functions import find_user
from keyboards.main_menu import main_kb

edit_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📅 День', callback_data='edit_day'),
     InlineKeyboardButton(text='🕑 Время рассылки', callback_data='edit_time')],
    [InlineKeyboardButton(text='🎓 Группа', callback_data='edit_group'),
     InlineKeyboardButton(text='🏢 Отделение', callback_data='edit_department')],
    [InlineKeyboardButton(text='📌 Быстрая кнопка', callback_data='edit_hotkey'),
     InlineKeyboardButton(text='⚙️ Стиль отображения', callback_data='edit_settings')],
    [InlineKeyboardButton(text='⛔ Прекратить отправку сообщений', callback_data='stop')]])

edit_day_kb = [
    [InlineKeyboardButton(text='Сегодня', callback_data='send_today')],
    [InlineKeyboardButton(text='Завтра', callback_data='send_tomorrow')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]]

edit_department_kb = [
    [InlineKeyboardButton(text='Дневное отделение', callback_data='department_full_time')],
    [InlineKeyboardButton(text='Другое', callback_data='department_other')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]]

edit_settings_kb = [[
    InlineKeyboardButton(text='Простое', callback_data='default_settings')],
    [InlineKeyboardButton(text='Подробное', callback_data='detailed_settings')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]]

edit_hotkey_kb = [[
    InlineKeyboardButton(text='Расписание на сегодня', callback_data='today_hotkey'),
    InlineKeyboardButton(text='Расписание на завтра', callback_data='tomorrow_hotkey')],
    [InlineKeyboardButton(text='Расписание на неделю', callback_data='full_hotkey')],
    [InlineKeyboardButton(text='Назад', callback_data='back')]]

delete_user_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗑️ Да', callback_data='delete_user')],
    [InlineKeyboardButton(text='🙅 Нет', callback_data='dont_delete_user')]])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]])


async def update_kb(kb: list, message: Message):
    user = await find_user(message.chat.id)

    if kb == edit_day_kb:
        field = 'day'
    elif kb == edit_department_kb:
        field = 'department'
    elif kb == edit_settings_kb:
        field = 'settings'
    else:
        field = 'hotkey'

    if kb == 'main':
        kb = copy.deepcopy(main_kb)
        kb.keyboard[0][0] = user['hotkey']
    else:
        kb = copy.deepcopy(kb)
        for i in range(len(kb)):
            btn = kb[i][0]
            if user[field] == btn.text:
                text = f'✅ {btn.text}'
            else:
                text = btn.text
            kb[i][0].text = text

    return InlineKeyboardMarkup(inline_keyboard=kb)
