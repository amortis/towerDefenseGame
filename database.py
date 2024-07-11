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

def get_username(user_id):
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def save_level_record(user_id, level, score):
    """
    Сохранить рекорд по user_id
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    # Check if record exists
    cursor.execute('''
    SELECT score FROM level_records WHERE user_id = ? AND level = ?
    ''', (user_id, level))
    record = cursor.fetchone()

    if record is None:
        # No record exists, insert new record
        cursor.execute('''
        INSERT INTO level_records (user_id, level, score) VALUES (?, ?, ?)
        ''', (user_id, level, score))
    elif score > record[0]:
        # Record exists and new score is higher, update record
        cursor.execute('''
        UPDATE level_records SET score = ? WHERE user_id = ? AND level = ?
        ''', (score, user_id, level))

    conn.commit()
    conn.close()


def get_level_records(user_id):
    """
    Получить рекорды по user_id
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT level, score FROM level_records WHERE user_id = ?
    ''', (user_id,))

    records = cursor.fetchall()
    conn.close()
    return records

def get_level_record(user_id, level):
    """
    Получить рекорд по user_id и level
    """
    conn = sqlite3.connect('tower_defense.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT level, score FROM level_records WHERE user_id = ? AND level = ?
        ''', (user_id, level))

    record = cursor.fetchall()
    conn.close()
    return record[0][1]

save_level_record(1,1,120)