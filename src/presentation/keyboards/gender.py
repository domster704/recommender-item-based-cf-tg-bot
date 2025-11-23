from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def gender_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
