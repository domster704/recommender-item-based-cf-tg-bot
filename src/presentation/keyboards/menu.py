from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Список фильмов")
    keyboard.button(text="Профиль")
    return keyboard.as_markup(resize_keyboard=True)
