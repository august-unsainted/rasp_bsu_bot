from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from handlers.get import cmd_get
from handlers.edit import cmd_edit
from handlers.help import cmd_help

router = Router()


@router.message(Command('edit'))
async def edit(message: Message):
    await cmd_edit(message)


@router.message(Command('get'))
async def get(message: Message):
    await cmd_get(message)


@router.message(Command('help'))
async def get_help(message: Message):
    await cmd_help(message)


@router.message()
async def any_message(message: Message):
    await message.answer('Я не понимаю Вас 😓\n'
                         'Пожалуйста, используйте команды или меню для общения со мной 🤖')
