from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from handlers.registration import Register
from utils.db_functions import update_user, find_user
from keyboards.edit import edit_settings_kb, edit_kb, edit_day_kb, edit_hotkey_kb, edit_department_kb, back_kb
from keyboards.main_menu import main_kb

router = Router()


@router.message(F.text == 'Изменить информацию')
async def cmd_edit(message: Message):
    await message.answer('Что Вы хотите отредактировать?', reply_markup=edit_kb)
    await message.delete()


@router.callback_query(F.data == 'edit_day')
async def edit_day(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Данные для изменения успешно выбраны')
    await state.set_state(Register.day)
    kb = edit_day_kb
    user = await find_user(callback.message.chat.id)
    if user['day'] == 'Сегодня':
        kb[0][0].text = '✅ Сегодня'
    else:
        kb[1][0].text = '✅ Завтра'

    await callback.message.edit_text('Выберите, на какой день отправлять расписание:',
                                     reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))


@router.callback_query(F.data == 'edit_time')
async def edit_time(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.time)
    await callback.message.edit_text('Напишите время отправки расписания (например, 00:00)', reply_markup=back_kb)


@router.callback_query(F.data == 'edit_group')
async def edit_group(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.group)
    await callback.message.edit_text('Введите номер группы (как в расписании)', reply_markup=back_kb)


@router.callback_query(F.data == 'edit_department')
async def edit_year(callback: CallbackQuery):
    await callback.message.edit_text('Выберите отделение для отправки расписания:', reply_markup=edit_department_kb)


@router.callback_query(F.data == 'edit_hotkey')
async def edit_settings(callback: CallbackQuery):
    await callback.answer('Данные для изменения успешно выбраны')
    await callback.message.edit_text('Выберите быструю кнопку:', reply_markup=edit_hotkey_kb)


@router.callback_query(F.data.endswith('hotkey'))
async def set_settings(callback: CallbackQuery):
    await callback.answer('Быстрая кнопка выбрана успешно')
    await callback.message.edit_text('Быстрая кнопка изменена успешно!')
    await callback.message.answer('Для изменения других данных воспользуйтесь меню',
                                  reply_markup=main_kb[int(callback.data[0])])


@router.callback_query(F.data == 'edit_settings')
async def edit_settings(callback: CallbackQuery):
    await callback.message.edit_text('Выберите тип отображения расписания:', reply_markup=edit_settings_kb)


@router.callback_query(F.data.endswith('settings'))
async def settings(callback: CallbackQuery):
    settings_type = callback.data.split('_')[0]
    await update_user(callback.message.chat.id, {"settings": settings_type})
    await callback.answer('Настройки изменены успешно')
    await callback.message.edit_text('Тип отображения был успешно изменен')


@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Что Вы хотите отредактировать?', reply_markup=edit_kb)
