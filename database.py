import aiosqlite

async def init_db():
    async with aiosqlite.connect("employees.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                manager_id INTEGER NOT NULL,
                full_name TEXT NOT NULL,
                birthday TEXT NOT NULL
            )
        ''')
        await db.commit()

async def add_employee(manager_id, full_name, birthday):
    async with aiosqlite.connect("employees.db") as db:
        await db.execute('''
            INSERT INTO employees (manager_id, full_name, birthday)
            VALUES (?, ?, ?)
        ''', (manager_id, full_name, birthday))
        await db.commit()

async def get_employees(manager_id):
    async with aiosqlite.connect("employees.db") as db:
        cursor = await db.execute('''
            SELECT id, full_name, birthday FROM employees
            WHERE manager_id = ?
        ''', (manager_id,))
        return await cursor.fetchall()

async def delete_employee(employee_id):
    async with aiosqlite.connect("employees.db") as db:
        await db.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        await db.commit()