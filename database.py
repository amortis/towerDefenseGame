import hashlib
import sqlite3


def register_user(username, password):
    """
    Регистрация пользователя в дб
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    # Хэширование пароля
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute('''
        INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, password_hash))
        conn.commit()
        print("User registered successfully!")
        return True
    except sqlite3.IntegrityError:
        print("Username already exists!")

    conn.close()


def login_user(username, password):
    """
    Авторизация пользователя в дб
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    # Хэширование пароля
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password_hash))

    user = cursor.fetchone()
    conn.close()

    if user:
        print("Login successful!")
        return user[0]  # Возвращаем id пользователя
    else:
        print("Invalid username or password!")
        return None


def save_level_record(user_id, level, score):
    """
    Сохранить рекорд по user_id
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO level_records (user_id, level, score) VALUES (?, ?, ?)
    ''', (user_id, level, score))
    conn.commit()
    conn.close()


def get_level_records(user_id):
    """
    Получить рекорд по user_id
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT level, score FROM level_records WHERE user_id = ?
    ''', (user_id,))

    records = cursor.fetchall()
    conn.close()
    return records
