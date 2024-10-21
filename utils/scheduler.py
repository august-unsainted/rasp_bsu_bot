import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from aiogram import Bot
from pymongo import MongoClient

from utils.db_functions import find_user
from utils.parser import get_rasp
from config import TOKEN, CLIENT

client = MongoClient(CLIENT)

jobstores = {
    'default': MongoDBJobStore(database='rasp_bsu', client=client)
}
os.environ['TZ'] = 'Asia/Irkutsk'
scheduler = AsyncIOScheduler(timezone='Asia/Irkutsk', jobstores=jobstores)


async def send_rasp(_id):
    user = await find_user(_id)
    message_text = await get_rasp(_id, user['day'], None)
    async with Bot(token=TOKEN) as bot:
        if message_text != 'К сожалению, на этот день нет расписания':
            await bot.send_message(_id, message_text, parse_mode='HTML')
        else:
            message_text = (f'На {user['day'].lower()} расписания нет! 🤩️\n'
                            'Это прекрасная возможность расслабиться и уделить время себе!\n'
                            'Хорошего отдыха ☺️')
            await bot.send_message(_id, message_text)


def add_schedule(user):
    time = user['time']
    scheduler.add_job(send_rasp, 'cron', hour=time[:2], minute=time[3:], id=str(user['_id']),
                      args=[user['_id']], replace_existing=True, misfire_grace_time=100)


def delete_schedule(user_id):
    scheduler.remove_job(str(user_id))


def pause_schedule(user_id):
    scheduler.get_job(str(user_id)).pause()


def resume_schedule(user_id):
    scheduler.get_job(str(user_id)).resume()
