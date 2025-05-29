import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from django.conf import settings

async def send_tg_message_async(chat_id: int | str, text: str):
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    await bot.send_message(chat_id, text)
    await bot.session.close()

def send_telegram_notification(message: str):
    try:
        chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
        asyncio.run(send_tg_message_async(chat_id, message))
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")