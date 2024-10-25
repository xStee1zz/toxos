import asyncio 
import logging 
import random 
 
import httpx 
import aiofiles 
from aiogram import Bot, Dispatcher 
from aiogram.filters import Command, CommandStart 
from aiogram.types import Message 
from aiogram.fsm.storage.memory import MemoryStorage 
from aiogram.fsm.state import State, StatesGroup 
from aiogram.fsm.context import FSMContext 
 
logging.basicConfig(level=logging.INFO) 
 
class UserId(StatesGroup): 
    user_id = State() 
 
 
bot = Bot(token='7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64') 
dp = Dispatcher(storage=MemoryStorage()) 
 
 
@dp.message(CommandStart()) 
async def start(message: Message) -> None: 
    await message.answer("Функции доступны в @null_dev") 
 
 
@dp.message(Command("spam")) 
async def spam(message: Message, state: FSMContext) -> None: 
    if message.chat.id == -1002018886275: 
        await message.reply("Введите ID игрока") 
        await state.set_state(UserId.user_id) 
    else: 
        await message.reply("Команда может быть выполнена в @null_dev") 
 
 
async def send_post_request(client, url, headers, data): 
    response = await client.post(url, headers=headers, json=data) 
    return response 
 
 
@dp.message(UserId.user_id) 
async def spam_run(message: Message, state: FSMContext) -> None: 
    async with aiofiles.open('bot.txt', mode='r') as file: 
        lines = await file.readlines() 
 
    success = 0 
 
    url = "https://gw.sandboxol.com/friend/api/v1/friends" 
     
    async with httpx.AsyncClient() as client: 
        tasks = [] 
 
        for _ in range(50): 
            random_line = random.choice(lines).strip() 
            bot_id, bot_token = random_line.split(':') 
 
            headers = { 
                "userId": bot_id, 
                "Access-Token": bot_token, 
                "User-Agent": "okhttp/4.11.0" 
            } 
            data = { 
                "friendId": message.text, 
                "msg": "" 
            } 
 
            tasks.append(send_post_request(client, url, headers, data)) 
 
        responses = await asyncio.gather(*tasks) 
 
        for response in responses: 
            response_json = response.json() 
            if 'message' in response_json and response_json['message'] == "SUCCESS": 
                success += 1 
 
    await message.reply(f"Отправлено {success} заявок!") 
 
    await state.clear() 
 
 
async def run(dp: Dispatcher) -> None: 
    await bot.send_message(-1002018886275, "Я запущен! Введи /spam, чтобы начать спам заявками") 
 
 
async def main() -> None: 
    await run(dp) 
    await dp.start_polling(bot) 
 
 
if __name__ == "__main__": 
    asyncio.run(main())
