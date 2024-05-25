from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Створює просту реплай-клавіатуру з кнопками в один ряд
    :param items: список текстів для кнопок
    :return: об'єкт реплай-клавіатури
    """
    keyboard = [[KeyboardButton(text=item)] for item in items]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)