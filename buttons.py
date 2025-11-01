from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="yes"), KeyboardButton(text='no')]
    ], resize_keyboard=True,
       one_time_keyboard=True
)