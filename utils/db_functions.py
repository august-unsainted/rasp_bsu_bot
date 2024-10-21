import motor.motor_asyncio
from config import CLIENT

cluster = motor.motor_asyncio.AsyncIOMotorClient(CLIENT)
collection = cluster.rasp_bsu.users


def add_user(chat_id, day, time, group, department):
    collection.insert_one({
        "_id": chat_id,
        "day": day,
        "time": time,
        "rasp_link": 'https://bsu.ru/rasp/?g=' + group,
        "department": department,
        "settings": 'Простое'
    })


def update_user(chat_id, data):
    return collection.update_one({"_id": chat_id}, {"$set": data})


def delete_user(chat_id):
    collection.delete_one({"_id": chat_id})


def find_user(user_id):
    return collection.find_one({"_id": user_id})
