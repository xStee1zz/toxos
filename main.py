import asyncio
import re
import random

import aiohttp
import aiofiles
from aiohttp.client_exceptions import ContentTypeError
import nest_asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

nest_asyncio.apply()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*Мой функционал исключительно для чатов @nullowns\\.\n\nДля того чтобы использовать мои функции, присоединись к нашему комьюнити в @null\\_dev\\.*",
        parse_mode="MarkdownV2"
    )


async def POST(session, url, headers, data):
    async with session.post(url, headers=headers, json=data) as response:
        try:
            return await response.json()
        except ContentTypeError:
            return None


async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 1 and re.match(r'^\d+$', context.args[0]):
        number = context.args[0]

        async with aiofiles.open('bot.txt', mode='r') as file:
            bot = await file.readlines()

        success = 0

        url = "https://gw.sandboxol.com/friend/api/v1/friends"

        data = {
            "friendId": number,
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

        await update.message.reply_text(
            f"*Отправлено \\{success} заявок\\!\n\nВозможные проблемы:\n • Заявки заполнены\n • Заявки отключены\n • Неверный ID*",
            parse_mode="MarkdownV2"
        )
    else:
        await update.message.reply_text(
            "*Неверный формат\\.\n\nВведите /spam ID*",
            parse_mode="MarkdownV2"
        )


async def main() -> None:
    app = Application.builder().token("7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64").build()

    app.add_handler(MessageHandler(filters.COMMAND & filters.ChatType.PRIVATE, echo))
    app.add_handler(CommandHandler("spam", spam))

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
