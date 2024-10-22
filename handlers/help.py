from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.get_help import help_kb, back_help_kb

router = Router()


@router.message(F.text == 'Помощь')
async def cmd_help(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    await message.answer('Выберите раздел:', reply_markup=help_kb)
    await message.delete()


@router.callback_query(F.data == 'about')
async def cmd_about(callback: CallbackQuery):
    await callback.message.edit_text('📝  Основная информация: '
                                     '<blockquote>Данный бот предназначен для удобного поиска расписания и отправки '
                                     'его по времени</blockquote>\n\n'
                                     '🤖 Функции бота:'
                                     '<blockquote>С помощью этого бота Вы можете получать расписание:\n'
                                     '• Ежедневно в выбранное Вами время\n'
                                     '• По запросу — быстро и удобно\n'
                                     '• В подходящем для Вас виде — простом или подробном</blockquote>\n\n'
                                     '❓ Основные обозначения:\n'
                                     '<blockquote>🧪 — Лабораторная\n'
                                     '🛠 — Практика\n'
                                     '✍️ — Лекция\n'
                                     '☠️ — Экзамен\n'
                                     '😰 — Зачёт</blockquote>', parse_mode='HTML', reply_markup=back_help_kb)


@router.callback_query(F.data == 'feedback')
async def cmd_about(callback: CallbackQuery):
    await callback.message.edit_text('Если у Вас есть вопросы, предложения или замечания по работе бота, '
                                     'не стесняйтесь написать @Feedback_rasp_bot для обратной связи 💡\n\n'
                                     'Мы будем рады обсудить любые вопросы 😊', reply_markup=back_help_kb)


@router.callback_query(F.data == 'help_back')
async def back_help(callback: CallbackQuery):
    await callback.message.edit_text('Выберите раздел:', reply_markup=help_kb)
