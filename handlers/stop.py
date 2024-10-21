from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.filters import Command

from utils.scheduler import pause_schedule, resume_schedule, delete_schedule
from utils.db_functions import delete_user
from keyboards.edit import delete_user_kb

router = Router()


@router.callback_query(F.data == 'stop')
async def cmd_stop(callback: CallbackQuery):
    await callback.answer('Данные для изменения успешно выбраны')
    await callback.message.edit_text('Вы уверены, что хотите продолжить? '
                                     'Эта команда приведёт сбросу всех ваших настроек 😨', reply_markup=delete_user_kb)


@router.callback_query(F.data.endswith('delete_user'))
async def callback_start(callback: CallbackQuery):
    await callback.answer('Вариант выбран')
    if callback.data == 'dont_delete_user':
        await callback.message.edit_text('Информация не была удалена. Для изменения данных воспользуйтесь меню ✅')
    else:
        delete_user(callback.message.chat.id)
        delete_schedule(callback.message.chat.id)
        await callback.message.edit_text('Данные были успешно удалены 😢')
        await callback.message.answer('Если у Вас есть вопросы, предложения или замечания по работе бота, '
                                      'не стесняйтесь написать @Feedback_rasp_bot для обратной связи 💡\n\n'
                                      'Мы будем рады обсудить любые вопросы 😊\n\n'
                                      '💬 Для повторной регистрации используйте команду /start',
                                      reply_markup=ReplyKeyboardRemove())


@router.message(Command('pause'))
async def cmd_pause(message: Message):
    pause_schedule(message.chat.id)
    await message.answer('Отправка сообщений временно прекращена.\n'
                         'Для возобновления отправки воспользуйтесь командой /resume')


@router.message(Command('resume'))
async def cmd_resume(message: Message):
    resume_schedule(message.chat.id)
    await message.answer('Отправка сообщений возобновлена! Для изменения данных воспользуйтесь меню')
