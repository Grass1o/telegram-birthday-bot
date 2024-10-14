from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    buttons = [
        [KeyboardButton('Показать список ваших сотрудников')],
        [KeyboardButton('Добавить день рождения нового сотрудника')],
        [KeyboardButton('Как работают уведомления')],
        [KeyboardButton('Удалить сотрудника')]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
