import logging
from datetime import datetime, timedelta
from database import get_employees
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Логирование
logging.basicConfig(level=logging.INFO)

def schedule_notifications(application):
    scheduler = AsyncIOScheduler()

    # Запускаем задачу для отправки уведомлений в 13:00
    scheduler.add_job(lambda: send_birthday_notifications(application), 'cron', hour=13, minute=0)
    scheduler.start()

async def send_birthday_notifications(application):
    # Получаем всех сотрудников из базы данных
    for user_id in application.bot_data.keys():
        employees = get_employees(user_id)
        today = datetime.today().date()

        for employee in employees:
            birthday = datetime.strptime(employee['birthday'], '%d.%m.%Y').date()
            days_until_birthday = (birthday.replace(year=today.year) - today).days

            # Если день рождения через 30, 14, 7 или 1 день
            if days_until_birthday in [30, 14, 7, 1]:
                try:
                    # Отправляем уведомление в чат
                    await application.bot.send_message(
                        chat_id=user_id,
                        text=f"Напоминание: День рождения {employee['name']} через {days_until_birthday} дней!"
                    )
                except Exception as e:
                    logging.error(f"Ошибка отправки уведомления пользователю {user_id}: {e}")
