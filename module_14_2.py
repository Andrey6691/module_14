import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                 (f"User{i}", f"example{i*10}@gmail.com", f'{i*10}', '1000'))


cursor.execute("UPDATE Users SET balance = 500 WHERE id IN (1, 3, 5, 7, 9)")

cursor.execute("DELETE FROM Users WHERE id in (1, 4, 7, 10)")

cursor.execute("SELECT Username, email, age, balance FROM Users WHERE age != ?", (60,))

cursor.execute("DELETE FROM Users WHERE id = 6")
#


# cursor.execute("DELETE FROM Users WHERE AGE > ?", ("5",))                    # удалить данные из таблицы

cursor.execute('SELECT COUNT(*) FROM Users')

total_users = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]

users = cursor.fetchall()
for user in users:
  print(f'Имя:{user[0]}, Почта: {user[1]}, Возраст: {user[2]}, Баланс:{user[3]}')
print(f'Итого пользователей: {total_users}, Общий баланс: {all_balances},Средний баланс: {all_balances / total_users}')


connection.commit()
connection.close()