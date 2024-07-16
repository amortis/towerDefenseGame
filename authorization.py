import tkinter as tk
from tkinter import messagebox
import database  # Импорт функций из database.py
import menu


# Функции для обработки регистрации и входа
def register():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        success = database.register_user(username, password)
        if success is not None:
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        else:
            messagebox.showerror("Ошибка", "Имя пользователя уже существует!")
    else:
        messagebox.showwarning("Предупреждение", "Поля не могут быть пустыми!")


def login():
    username = username_entry.get()
    password = password_entry.get()
    if username and password:
        user_id = database.login_user(username, password)
        if user_id:
            messagebox.showinfo("Успех", "Вход выполнен успешно!")
            root.destroy()
            # Переход к следующей части игры
            m = menu.Menu(user_id)
            m.run()
        else:
            messagebox.showerror("Ошибка", "Ошибка входа!")
    else:
        messagebox.showwarning("Предупреждение", "Поля не могут быть пустыми!")

database.create_database()
# Создание окна
root = tk.Tk()
root.title("Стражи пути - Вход")

# Настройки окна
root.geometry("400x300")

# Метки и поля ввода
tk.Label(root, text="Имя пользователя:").pack(pady=10)
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

tk.Label(root, text="Пароль:").pack(pady=10)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

# Кнопки
tk.Button(root, text="Вход", command=login).pack(pady=10)
tk.Button(root, text="Регистрация", command=register).pack(pady=5)

# Запуск основного цикла
root.mainloop()
