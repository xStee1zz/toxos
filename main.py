import asyncio
import logging
import random

import aiofiles
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
 
class UserId(StatesGroup):
    user_id = State()

bot = Bot(token='7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64')
dp = Dispatcher(storage=MemoryStorage())


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer("Функции доступны в @null_dev")


@dp.message(Command("spam"))
async def spam(message: Message, state: FSMContext):
    if message.chat.id == -1002018886275:
        await message.reply("Введите ID игрока")
        await state.set_state(UserId.user_id)
    else:
        await message.reply("Команда может быть выполнена в @null_dev")


async def POST(session, url, headers, data):
    async with session.post(url, headers=headers, json=data) as response:
        try:
            return await response.json()
        except ContentTypeError:
            return None


@dp.message(UserId.user_id)
async def spam_run(message: Message, state: FSMContext):
    async with aiofiles.open('bot.txt', mode='r') as file:
        bot = await file.readlines()

    success = 0

    url = "https://gw.sandboxol.com/friend/api/v1/friends"

    data = {
        "friendId": message.text,
        "msg": ""
    }

    async with aiohttp.ClientSession() as session:
        tasks = []

        for _ in range(100):
            bot_id, bot_token = random.choice(bot).strip().split(':')

            headers = {
                "userId": bot_id,
                "Access-Token": bot_token,
                "Content-Type": "application/json",
                "User-Agent": "okhttp/4.11.0"
            }

            tasks.append(POST(session, url, headers, data))

        responses = await asyncio.gather(*tasks)

        for response in responses:
            if response is None:
                continue
            if 'message' in response and response['message'] == "SUCCESS":
                success += 1

    await message.reply(f"Отправлено {success} заявок!\n\nВозможные проблемы:\n • Заявки заполнены\n • Заявки отключены\n • Неверный ID")
    await state.clear()


async def on_startup():
    await bot.send_message(-1002018886275, "Уважаемые игроки!\n\nДоступен спам в друзья до 100 заявок - /spam") 


async def main():
    await on_startup() 
    await dp.start_polling(bot) 


if __name__ == "__main__":
    asyncio.run(main())
