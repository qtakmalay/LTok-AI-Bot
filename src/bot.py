import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import settings
from src.qa_agent import answer_question, initialize_agent

initialize_agent()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Hello! Ask me any question about the loaded website content.")

@dp.message()
async def handle_question(message: types.Message):
    user_question = message.text.strip()
    await message.answer("Let me think...")

    loop = asyncio.get_running_loop()
    answer = await loop.run_in_executor(None, answer_question, user_question)

    await message.answer(f"{answer}")

async def start_bot():
    print("Bot is starting...")
    await dp.start_polling(bot, skip_updates=True)
