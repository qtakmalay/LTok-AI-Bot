# src/bot.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import settings
from src.qa_agent import answer_question, initialize_agent

initialize_agent()

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

commands = [
    types.BotCommand(command="start", description="Start interacting with bot"),
    types.BotCommand(command="help", description="Show help information"),
]

async def set_commands(bot: Bot):
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    welcome_message = (
        "Welcome to the LATOKEN Talent Bot! 🎉 We are excited to have you explore opportunities with us. "
        "LATOKEN is a cutting-edge crypto exchange and Web3 platform on a mission to democratize capital markets "
        "and “find the next bitcoin before others.” Our motto is “Go global to grow with frontier tech to change the world.”\n\n"
        "This bot will guide you through information about LATOKEN’s talent programs, culture, and events. You’ll learn how we help "
        "launch the next Web3 gems for early adopters, and how our team’s vision is to empower billions of people to trade millions of assets, "
        "pushing the boundaries of finance and technology.\n\n"
        "Feel free to explore and ask questions. Let’s build the future together with LATOKEN Talent! 🚀"
    )
    await message.answer(welcome_message)

@dp.message(Command("help"))
async def send_help(message: types.Message):
    help_text = (
        "You can interact with the LATOKEN Talent Bot through text commands or by using the menu buttons. Here’s how to get started:\n\n"
        "• Ask Questions: Simply type your question to inquire about LATOKEN’s hackathon schedule, company mission, culture, and more.\n"
        "• Commands: Use /start to see the welcome message again or /help to view these instructions.\n"
        "If you need further assistance, just ask!"
    )
    await message.answer(help_text)

@dp.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data == "ask_question":
        await callback_query.message.answer("Please type your question about LATOKEN.")
    elif data == "view_schedule":
        await callback_query.message.answer(
            "LATOKEN Talent events schedule:\n• Hackathon stage starts after the initial interviews.\n• Detailed timelines will be provided upon qualification.\nFor more details, please ask your question."
        )
    elif data == "about_latoken":
        await callback_query.message.answer(
            "LATOKEN is a leading crypto exchange and Web3 platform committed to democratizing capital markets and launching the next wave of innovative blockchain projects. "
            "We empower billions of people to trade millions of assets and drive financial inclusion."
        )
    elif data == "help_info":
        await callback_query.message.answer("Use /help to see instructions or type your question directly.")
    await callback_query.answer()

@dp.message()
async def handle_question(message: types.Message):
    user_question = message.text.strip()
    thinking_msg = await message.answer("⏳ Let me think...")
    loop = asyncio.get_running_loop()
    answer = await loop.run_in_executor(None, answer_question, user_question)
    await thinking_msg.edit_text(answer)

async def start_bot():
    print("🚀 Bot is starting...")
    await set_commands(bot)
    await dp.start_polling(bot, skip_updates=True)
