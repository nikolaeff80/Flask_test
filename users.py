import sqlite3
import random


class User:
    def __init__(self):
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
        self.create_sample_data()

    def create_table(self):
        """Создаем таблицу пользователей в базе данных."""
        self.cursor.execute('''DROP TABLE IF EXISTS users''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                balance INTEGER NOT NULL)''')
        self.conn.commit()
    
    def create_sample_data(self):
        """Добавляем тестовые данные в базу данных."""
        try:
            for i in range(1, 6):
                username = f'user_{i}'
                balance = random.randint(5000, 15000)
                self.cursor.execute('''INSERT INTO users (username, balance) VALUES (?, ?)''', (username, balance))
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    def add_user(self, username, balance):
        """Добавление нового пользователя в базу данных"""
        self.cursor.execute('''INSERT INTO users (username, balance) VALUES (?, ?)''', (username, int(balance)))
        self.conn.commit()

    def update_balance(self, user_id, new_balance):
        """Обновление баланса выбранного пользователя"""
        self.cursor.execute('''UPDATE users SET balance = ? WHERE id = ?''', (new_balance, int(user_id)))
        self.conn.commit()
    
    def update_user(self, user_id, new_username):
        """Обновление данных выбранного пользователя"""
        self.cursor.execute('''UPDATE users SET username = ? WHERE id = ?''', (new_username, int(user_id)))
        self.conn.commit()
        
    def delete_user(self, user_id):
        """Удаление выбранного пользователя из базы данных"""
        self.cursor.execute('''DELETE FROM users WHERE id = ?''', (int(user_id),))
        self.conn.commit()
    
    def get_all_users(self):
        """Возвращает список всех пользователей из базы данных."""
        try:
            self.cursor.execute('''SELECT * FROM users''')
        except sqlite3.Error as e:
            print("SQLite error:", e.args[0])
        users = self.cursor.fetchall()
        return users
    
    def get_balance(self, user_id):
        """Получает баланс пользователя по его user_id из базы данных."""
        self.cursor.execute('''SELECT balance FROM users WHERE id = ?''', (user_id,))
        balance = self.cursor.fetchone()
        if balance:
            return balance[0]
        else:
            return None
        