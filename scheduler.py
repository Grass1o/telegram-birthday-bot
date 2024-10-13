from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
import datetime
from database import get_employees

def send_notification(bot, chat_id, employee, days_left):
    bot.send_message(chat_id, text=f"До дня рождения {employee['name']} осталось {days_left} дней!")

def schedule_notifications(application):
    scheduler = BackgroundScheduler()
    bot = Bot(token='YOUR_TELEGRAM_BOT_TOKEN')

    def check_birthdays():
        for manager_id in application.persistence.get_user_ids():
            employees = get_employees(manager_id)
            today = datetime.date.today()

            for employee in employees:
                birthday = datetime.datetime.strptime(employee['birthday'], "%d.%m.%Y").date()
                delta = birthday - today

                if delta.days in [30, 14, 7, 1]:
                    send_notification(bot, manager_id, employee, delta.days)

    scheduler.add_job(check_birthdays, 'interval', hours=24)
    scheduler.start()
