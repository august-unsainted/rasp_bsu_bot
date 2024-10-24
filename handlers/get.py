from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from utils.db_functions import find_user
from utils.parser import get_rasp, edit_week_length
from utils.time_functions import find_rasp
from handlers.registration import cmd_start
from keyboards.get_rasp import curr_week_kb, get_rasp_kb, back_rasp_kb, back_parity_kb, close_kb

router = Router()


@router.message(F.text == 'Получить расписание')
async def cmd_get(message: Message):
    await message.answer('Выберите, какое расписание Вам отправить:', reply_markup=get_rasp_kb)
    await message.delete()


@router.callback_query(F.data == 'rasp_back')
async def cmd_get_rasp(callback: CallbackQuery):
    await callback.message.edit_text('Выберите, какой прогноз Вам отправить:', reply_markup=get_rasp_kb)


@router.callback_query(F.data.endswith('rasp'))
async def send_rasp(callback: CallbackQuery, state: FSMContext):
    user = await find_user(callback.message.chat.id)
    if user and callback.data == 'week_rasp':
        if user["department"] == 'Дневное отделение':
            await callback.answer('Тип расписания выбран успешно!')
            await callback.message.edit_text('Выберите номер недели:', reply_markup=curr_week_kb())
        else:
            text = await get_rasp(callback.message.chat.id, 'week', 0)
            texts = edit_week_length(text)
            await callback.answer('Тип расписания выбран успешно!')
            await callback.message.edit_text(texts[0], parse_mode='HTML', reply_markup=back_rasp_kb)
            if len(texts) > 1:
                for mess in texts[1:]:
                    await callback.message.answer(mess, parse_mode='HTML', reply_markup=back_rasp_kb)
    elif user:
        rasp_type = callback.data.replace('_rasp', '')
        if rasp_type == 'tomorrow':
            rasp_type = 'Завтра'
        text = await get_rasp(user['_id'], rasp_type, '')
        await callback.answer('Тип расписания выбран успешно!')
        await callback.message.edit_text(text, parse_mode='HTML',
                                         reply_markup=back_rasp_kb)
    else:
        await cmd_start(callback.message, state)


@router.message(F.text.startswith('Расписание на'))
async def send_rasp(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    user = await find_user(message.chat.id)
    if message.text == 'Расписание на неделю':
        if user['department'] == 'Другое':
            text = await get_rasp(message.chat.id, 'week', 0)
            texts = edit_week_length(text)
            for mess in texts:
                await message.answer(mess, parse_mode='HTML', reply_markup=close_kb)
        else:
            week_parity = find_rasp('Сегодня')[1]
            await message.answer(await get_rasp(message.chat.id, 'week', week_parity), parse_mode='HTML',
                                 reply_markup=close_kb)
        await message.delete()
    else:
        day = message.text[14:].capitalize()
        await message.answer(await get_rasp(message.chat.id, day, ''), parse_mode='HTML',
                             reply_markup=close_kb)
        await message.delete()


@router.callback_query(F.data.startswith('week_parity'))
async def full_time_rasp(callback: CallbackQuery):
    await callback.answer('Номер недели успешно выбран')
    week_parity = int(callback.data[-1]) - 1
    await callback.message.edit_text(await get_rasp(callback.message.chat.id, 'week', week_parity),
                                     parse_mode='HTML', reply_markup=back_parity_kb)


@router.callback_query(F.data == 'close')
async def close_rasp(callback: CallbackQuery):
    await callback.message.delete()
