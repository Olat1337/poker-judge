import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from main import ask_judge, setup_llm, EMBEDDING_MODEL_NAME, LLM_MODEL, CHROMA_PATH
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

llm = setup_llm(LLM_MODEL)
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hi! I'm a professional AI poker judge. Ask me anything!")

@dp.message()
async def judge_answer(message: types.Message):
    question = message.text
    await message.answer("The judge is flipping through the rulebook...")
    answer = ask_judge(question, db, llm)

    await message.answer(answer)

async def main():
    print("Bot started...")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())