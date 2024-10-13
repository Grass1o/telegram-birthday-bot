import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from database import add_employee, remove_employee, get_employees
from scheduler import schedule_notifications

# Логирование
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context):
    await update.message.reply_text(
        "Привет! Я бот для напоминания о днях рождения сотрудников. Вот команды:\n"
        "/add_employee - Добавить сотрудника в формате ФИО ДД.ММ.ГГГГ\n"
        "/remove_employee - Удалить сотрудника по его номеру"
    )

async def add_employee_command(update: Update, context):
    text = ' '.join(context.args)
    if add_employee(update.message.from_user.id, text):
        await update.message.reply_text(f'Сотрудник {text} добавлен!')
    else:
        await update.message.reply_text('Ошибка при добавлении. Проверьте формат.')

async def remove_employee_command(update: Update, context):
    employees = get_employees(update.message.from_user.id)
    if not employees:
        await update.message.reply_text('Список сотрудников пуст.')
        return

    list_text = "\n".join([f"{i}. {e['name']} - {e['birthday']}" for i, e in enumerate(employees)])
    await update.message.reply_text(f'Ваши сотрудники:\n{list_text}\nВведите номер для удаления.')

    # Ожидание ответа пользователя
    def handle_remove(update: Update, context):
        try:
            index = int(update.message.text)
            if remove_employee(update.message.from_user.id, index):
                update.message.reply_text('Сотрудник удален.')
            else:
                update.message.reply_text('Неверный номер.')
        except ValueError:
            update.message.reply_text('Пожалуйста, введите корректный номер.')

    context.application.add_handler(MessageHandler(filters.TEXT, handle_remove))

if __name__ == '__main__':
    # Получение токена из переменной окружения
    TOKEN = os.getenv('BOT_TOKEN')
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('add_employee', add_employee_command))
    app.add_handler(CommandHandler('remove_employee', remove_employee_command))

    schedule_notifications(app)  # Запуск планировщика

    app.run_polling()