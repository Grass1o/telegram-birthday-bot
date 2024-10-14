import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.utils.executor import start_polling
from config import BOT_TOKEN
from handlers import start_command, add_employee_handler, show_employees, delete_employee_handler, process_employee_data
from database import init_db

logging.basicConfig(filename='logs/bot.log', level=logging.INFO)

async def set_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Запустить бота")]
    await bot.set_my_commands(commands)

async def on_startup(dp: Dispatcher):
    await set_commands(dp.bot)
    await init_db()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(start_command, commands="start")
dp.register_message_handler(add_employee_handler, lambda message: message.text == 'Добавить день рождения нового сотрудника')
dp.register_message_handler(show_employees, lambda message: message.text == 'Показать список ваших сотрудников')
dp.register_message_handler(delete_employee_handler, lambda message: message.text == 'Удалить сотрудника')
dp.register_message_handler(process_employee_data)

if __name__ == "__main__":
    start_polling(dp, on_startup=on_startup)