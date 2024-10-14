import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, filters
from database import add_employee, remove_employee, get_employees
from scheduler import schedule_notifications  # Планировщик уведомлений
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Логирование
logging.basicConfig(level=logging.INFO)

# Состояния для разговора
ADD_EMPLOYEE = 1
REMOVE_EMPLOYEE = 2

# Основное меню с кнопками
def main_menu():
    keyboard = [
        ["Показать список ваших сотрудников"],
        ["Добавить день рождения нового сотрудника"],
        ["Удалить сотрудника"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Привет! Я бот для напоминания о днях рождения сотрудников.",
        reply_markup=main_menu()
    )

# Показать список сотрудников
async def list_employees(update: Update, context: CallbackContext):
    employees = get_employees(update.message.from_user.id)
    if not employees:
        await update.message.reply_text('Ваш список сотрудников пуст.')
    else:
        list_text = "\n".join([f"{i + 1}. {e['name']} - {e['birthday']}" for i, e in enumerate(employees)])
        await update.message.reply_text(f'Ваши сотрудники:\n{list_text}')

# Добавление сотрудника - просим ввести ФИО и дату
async def ask_for_employee_details(update: Update, context: CallbackContext):
    await update.message.reply_text("Пожалуйста, введите данные сотрудника в формате: ФИО ДД.ММ.ГГГГ")
    return ADD_EMPLOYEE

# Обработка введенного сотрудника
async def add_employee_command(update: Update, context: CallbackContext):
    text = update.message.text
    if add_employee(update.message.from_user.id, text):
        await update.message.reply_text(f'Сотрудник {text} добавлен!', reply_markup=main_menu())
    else:
        await update.message.reply_text('Ошибка при добавлении. Проверьте формат (ФИО ДД.ММ.ГГГГ).', reply_markup=main_menu())
    return ConversationHandler.END

# Удаление сотрудника - показать список и запросить номер
async def ask_for_employee_removal(update: Update, context: CallbackContext):
    employees = get_employees(update.message.from_user.id)
    if not employees:
        await update.message.reply_text('Список сотрудников пуст.')
        return ConversationHandler.END

    list_text = "\n".join([f"{i + 1}. {e['name']} - {e['birthday']}" for i, e in enumerate(employees)])
    await update.message.reply_text(f'Ваши сотрудники:\n{list_text}\nВведите номер сотрудника для удаления.')
    return REMOVE_EMPLOYEE

# Удаление сотрудника по номеру
async def remove_employee_command(update: Update, context: CallbackContext):
    try:
        index = int(update.message.text) - 1
        if remove_employee(update.message.from_user.id, index):
            await update.message.reply_text('Сотрудник удален.', reply_markup=main_menu())
        else:
            await update.message.reply_text('Неверный номер.', reply_markup=main_menu())
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите корректный номер.', reply_markup=main_menu())
    return ConversationHandler.END

if __name__ == '__main__':
    # Получение токена из переменной окружения
    TOKEN = os.getenv('BOT_TOKEN')
    app = ApplicationBuilder().token(TOKEN).build()

    # Планировщик уведомлений - перенос в scheduler.py
    scheduler = AsyncIOScheduler()
    scheduler.start()

    # Команды и разговоры
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^Добавить день рождения нового сотрудника$'), ask_for_employee_details),
            MessageHandler(filters.Regex('^Удалить сотрудника$'), ask_for_employee_removal),
        ],
        states={
            ADD_EMPLOYEE: [MessageHandler(filters.TEXT, add_employee_command)],
            REMOVE_EMPLOYEE: [MessageHandler(filters.TEXT, remove_employee_command)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Regex('^Показать список ваших сотрудников$'), list_employees))
    app.add_handler(conv_handler)

    app.run_polling()
