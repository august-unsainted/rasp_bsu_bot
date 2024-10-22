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


async def update_kb(field: str, message: Message) -> InlineKeyboardMarkup:
    user = await find_user(message.chat.id)
    fields = {
        'day': edit_day_kb,
        'department': edit_department_kb,
        'settings': edit_settings_kb,
        'hotkey': edit_hotkey_kb,
        'main': main_kb
    }
    kb = copy.deepcopy(fields[field])
    if field == 'main':
        kb.keyboard[0][0] = user['hotkey']
    else:
        for i in range(len(kb)):
            for j in range(len(kb[i])):
                btn = kb[i][j]
                if user[field] == btn.text:
                    kb[i][j].text = f'✅ {btn.text}'
                else:
                    kb[i][j].text = btn.text

    return InlineKeyboardMarkup(inline_keyboard=kb)
