from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from utils.db_functions import *
from utils.parser import group_validation, find_department
from utils.time_functions import time_validation
from utils.scheduler import add_schedule
from keyboards.edit import back_kb
from keyboards.main_menu import main_kb
from keyboards.registration import reg_day_kb, reg_department_kb

router = Router()


class Register(StatesGroup):
    day = State()
    group = State()
    time = State()
    department = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if await find_user(message.chat.id):
        await message.answer(
            'Вы уже зарегистрированы. Для изменения данных воспользуйтесь меню')
    else:
        await message.answer('Данный бот предназначен для удобного поиска расписания и отправки его по времени 📆\n\n'
                             'По всем вопросам: @Feedback_rasp_bot')
        await state.set_state(Register.day)
        await message.answer('Выберите, на какой день отправлять расписание:', reply_markup=reg_day_kb)


@router.callback_query(F.data.startswith('send'))
async def register_day(callback: CallbackQuery, state: FSMContext):
    await callback.answer('День выбран успешно')
    days = {'today': 'Сегодня', 'tomorrow': 'Завтра'}
    day = days[callback.data.split('_')[1]]
    if await find_user(callback.message.chat.id):
        update_user(callback.message.chat.id, {'day': day})
        await callback.message.edit_text('День успешно изменен! '
                                         'Для изменения других данных воспользуйтесь кнопкой:', reply_markup=back_kb)
        await state.clear()
    else:
        await state.update_data(day=day)
        await callback.message.edit_text('День выбран успешно!')
        await state.set_state(Register.time)
        await callback.message.answer('Напишите время отправки расписания (например, 00:00)')


@router.message(Register.time)
async def set_time(message: Message, state: FSMContext):
    time = time_validation(message.text)
    if time:
        await state.update_data(time=time)
        user = await find_user(message.chat.id)
        if user:
            await state.clear()
            await update_user(message.chat.id, {"time": time})
            add_schedule(await find_user(message.chat.id))
            await message.answer('Время отправки успешно изменено! '
                                 'Для изменения других данных воспользуйтесь кнопкой:', reply_markup=back_kb)
        else:
            await state.set_state(Register.group)
            await message.answer('Введите номер группы (как в расписании)')
    else:
        await message.answer('Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ (например, 00:00)')


async def end_registration(message: Message, state: FSMContext):
    _id = message.chat.id
    data = await state.get_data()
    await state.clear()
    add_user(_id, data['day'], data["time"], data["group"], data["department"])
    user = await find_user(_id)
    await message.answer(
        f'👀 Информация о Вас:<blockquote>'
        f'📅 День — {user["day"]}\n\n'
        f'🕓 Время — {user["time"]}\n\n'
        f'🎓 Номер группы — {user["rasp_link"][23:]}\n\n'
        f'🏢 Отделение — {user["department"]}</blockquote>\n\n'
        f'Для изменения данных воспользуйтесь меню ☺️', parse_mode='HTML', reply_markup=main_kb)
    add_schedule(user)


@router.message(Register.group)
async def set_group(message: Message, state: FSMContext):
    group = group_validation(message.text)
    if group:
        await state.update_data(group=group)
        if await find_user(message.chat.id):
            data = await state.get_data()
            await state.clear()
            update_user(message.chat.id, {"rasp_link": 'https://bsu.ru/rasp/?g=' + data["group"]})
            await message.answer('Номер группы успешно изменен! '
                                 'Для изменения других данных воспользуйтесь кнопкой:', reply_markup=back_kb)
        else:
            department = find_department(group)
            if department:
                await state.set_state(Register.department)
                await state.update_data(department=department)
                await end_registration(message, state)
            else:
                await message.answer('Выберите отделение для отправки расписания:', reply_markup=reg_department_kb)
    else:
        await message.answer('Неверный номер группы. Пожалуйста, введите номер группы (как в расписании)')


@router.callback_query(F.data.startswith('department'))
async def set_department(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    departments = {'department_full_time': 'Дневное отделение',
                   'department_other': 'Другое'}
    await state.set_state(Register.department)
    await state.update_data(department=departments[callback.data])
    _id = message.chat.id
    if await find_user(_id):
        update_user(_id, {"department": departments[callback.data]})
        await message.edit_text('Отделение успешно изменено! '
                                'Для изменения других данных воспользуйтесь кнопкой:', reply_markup=back_kb)
    else:
        await message.edit_text('Отлично! Теперь Вам будут приходить сообщения ✅')
        await end_registration(message, state)
