import sqlite3

def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        manager_id INTEGER,
        name TEXT,
        birthday TEXT
    )''')
    conn.commit()
    conn.close()

def add_employee(manager_id, text):
    try:
        name, birthday = text.rsplit(' ', 1)
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO employees (manager_id, name, birthday) VALUES (?, ?, ?)',
                       (manager_id, name, birthday))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_employees(manager_id):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, birthday FROM employees WHERE manager_id = ?', (manager_id,))
    employees = [{'name': row[0], 'birthday': row[1]} for row in cursor.fetchall()]
    conn.close()
    return employees

def remove_employee(manager_id, index):
    try:
        employees = get_employees(manager_id)
        if 0 <= index < len(employees):
            name = employees[index]['name']
            conn = sqlite3.connect('employees.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees WHERE manager_id = ? AND name = ?', (manager_id, name))
            conn.commit()
            conn.close()
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
