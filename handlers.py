from aiogram import types
from database import add_employee, get_employees, delete_employee
from keyboards import main_menu

async def start_command(message: types.Message):
    await message.answer("Привет! Я бот для напоминаний о днях рождения сотрудников. Вот что я умею:", reply_markup=main_menu())

async def add_employee_handler(message: types.Message):
    await message.answer("Введите данные сотрудника в формате: ФИО ДД.ММ.ГГГГ")

async def process_employee_data(message: types.Message):
    data = message.text.split(' ')
    if len(data) == 4 and validate_birthday(data[3]):
        await add_employee(message.from_user.id, ' '.join(data[:3]), data[3])
        await message.answer("Сотрудник добавлен.")
    else:
        await message.answer("Неверный формат. Попробуйте снова.")

async def show_employees(message: types.Message):
    employees = await get_employees(message.from_user.id)
    if employees:
        employee_list = '\n'.join([f"{idx}. {emp[1]} - {emp[2]}" for idx, emp in enumerate(employees, 1)])
        await message.answer(f"Ваши сотрудники:\n{employee_list}")
    else:
        await message.answer("Список пуст.")

async def delete_employee_handler(message: types.Message):
    employees = await get_employees(message.from_user.id)
    if employees:
        employee_list = '\n'.join([f"{idx}. {emp[1]} - {emp[2]}" for idx, emp in enumerate(employees, 1)])
        await message.answer(f"Ваши сотрудники:\n{employee_list}\nВведите номер сотрудника для удаления.")
    else:
        await message.answer("Список пуст.")
