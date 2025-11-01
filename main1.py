import logging
import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import Bot_token, kanal_id
from states import Step
from aiogram.fsm.context import FSMContext
from buttons import menu


dp = Dispatcher()
bot = Bot(token=Bot_token)
logging.basicConfig(level=logging.INFO)




@dp.message(CommandStart())
async def BotStart(message: Message):
    ism = message.from_user.full_name
    await message.answer(f"Assalomu aleykum {ism}\nDasturlash sohasiga qiziqasizmi?")


@dp.message(Command("help"))
async def HelpBot(message: Message):
    await message.answer(text="Botdan foydalanish uchun /start buyrug'ini yuboring")


@dp.message(F.text, Step.activity)
async def ActivityBot(message: Message, state: FSMContext):
    await message.answer("Qaysi dasturlash tilini o'rganmoqchisiz?")
    xabar = message.text
    await state.update_data({"language": xabar})
    await state.set_state(Step.language)

@dp.message(F.text, Step.language)
async def LanguageBot(message: Message, state: FSMContext):
    xabar = message.text
    data = await state.get_data()
    yes = data.get('yes')
    language = data.get('language')
    await state.update_data(framework=xabar)
    await message.answer(f"Siz tanlagan ma'lumotlar:\n\nActivity: {yes}\nProgramming language: {language}\nFramework: {xabar}", reply_markup=menu)
    await state.set_state(Step.send)


@dp.message(F.text=="yes", Step.send)
async def YesSendBot(message: Message, state: FSMContext):
    data = await state.get_data()
    yes = data.get('yes')
    language = data.get('language')
    framework = data.get('framework')
    await bot.send_message(chat_id=kanal_id, text=f"Ma'lumotlar:\n\nActivity: {yes}\nProgramming language: {language}\nFramework: {framework}")
    await state.clear()


@dp.message(F.text=="no", Step.send)
async def NoSendBot(message: Message, state: FSMContext):
    await message.answer("Ma'lumotlar yuborilmadi botni qayta ishga tushuring!")
    await state.clear()


@dp.message(F.text.title()=="Yes")
async def YesBot(message: Message, state: FSMContext):
    await message.answer("Qaysi yo'nalishga ko'proq qiziqasiz?")
    await state.update_data({"yes": message.text})
    await state.set_state(Step.activity)
    

@dp.message(F.text.title()=="No")
async def NoBot(message: Message):
    await message.answer("Siz bilan biz bog'lanamiz")







async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"The bot is over {e}")
