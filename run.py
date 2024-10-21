import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TOKEN
from handlers import registration, edit, stop, get, help, commands
from utils.scheduler import scheduler

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(registration.router, edit.router, stop.router, get.router, help.router, commands.router)
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # включаем только в процессе разработки, потом - выкл
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
