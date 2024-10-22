import motor.motor_asyncio
from config import CLIENT

cluster = motor.motor_asyncio.AsyncIOMotorClient(CLIENT)
collection = cluster.rasp_bsu.users


def add_user(chat_id: int, day: str, time: str, group: str, department: str) -> None:
    collection.insert_one({
        "_id": chat_id,
        "day": day,
        "time": time,
        "rasp_link": 'https://bsu.ru/rasp/?g=' + group,
        "department": department,
        "settings": 'Простое',
        "hotkey": 'Расписание на неделю'
    })


def update_user(chat_id: int, data: dict):
    return collection.update_one({"_id": chat_id}, {"$set": data})


def delete_user(chat_id: int) -> None:
    collection.delete_one({"_id": chat_id})


def find_user(user_id: int):
    return collection.find_one({"_id": user_id})
