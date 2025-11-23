from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def occupations_keyboard(occupations: list):
    rows = []
    row = []
    for o in occupations:
        row.append(KeyboardButton(text=o["name"]))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        one_time_keyboard=True,
    )
