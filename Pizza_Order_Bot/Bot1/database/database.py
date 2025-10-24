import json
import os
import sqlite3
from typing import List
from dotenv import load_dotenv

load_dotenv()


def clearUserOrder(telegram_id: int) -> None:
    with sqlite3.connect(os.getenv("SQLITE_PATH")) as connection:
        with connection:
            connection.execute(
                "UPDATE users SET state = NULL, _order = NULL WHERE telegram_id = ?",(telegram_id,)
            )

def updateUserOrder(telegram_id: int, data: dict) -> None:
    with sqlite3.connect(os.getenv("SQLITE_PATH")) as connection:
        with connection:
            connection.execute(
                "UPDATE users SET _order = ? WHERE telegram_id = ?",
                (json.dumps(data, ensure_ascii=False, indent=2), telegram_id)
            )

def updateUserStatus(telegram_id: int, waste_money: float) -> None:
    with sqlite3.connect(os.getenv("SQLITE_PATH")) as connection:
        with connection:
            connection.execute("""
                UPDATE users SET count = count + 1, money_waste = money_waste + ? WHERE telegram_id = ?""", (waste_money, telegram_id)
                )


def updateUserState(telegram_id: int, state: str) -> None:
    with sqlite3.connect(os.getenv("SQLITE_PATH")) as connection:
        with connection:
            connection.execute(
                "UPDATE users SET state = ? WHERE telegram_id = ?",(state, telegram_id)
            )

def getUser(telegram_id: int) -> dict | None:
    with sqlite3.connect(os.getenv("SQLITE_PATH")) as connection:
        with connection:
            cursor = connection.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'telegram_id': result[1],
                    'created_at': result[2],
                    'state': result[3],
                    '_order': result[4],
                    'count': result[5],
                    'money_waste': result[6]
                }
            return None

def all_tables_exists(table_names: List[str]) -> bool:
    """Проверяет существование всех таблиц из указанного списка в базе данных SQLite."""
    for table_name in table_names:
        if not table_exists(table_name):
            return False
    return True


def table_exists(table_name: str) -> bool:
    """Проверяет существование таблицы в базе данных SQLite."""
    try:
        with sqlite3.connect(os.getenv("SQLITE_PATH")) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """, (table_name,))
            return cursor.fetchone() is not None
    except TypeError:
        return False

def recreate_db() -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_PATH"))
    with connection:
        connection.execute("DROP TABLE IF EXISTS telegram_updates")
        connection.execute("""CREATE TABLE IF NOT EXISTS telegram_updates
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """)
        connection.execute("""CREATE TABLE IF NOT EXISTS users
            (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                state TEXT DEFAULT NULL,
                _order TEXT DEFAULT NULL,
                count INTEGER DEFAULT 0,
                money_waste REAL DEFAULT 0.0
            )
            """)

    connection.close()
    
def persist_updates(update:list) -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_PATH"))
    with connection:

        connection.executemany(
            "INSERT INTO telegram_updates (payload) VALUES (?)",
            [(json.dumps(update, ensure_ascii=True, indent=2),)]
                               )
        
    connection.close()
    
def ensure_user_exists(telegram_id: int) -> None:
    with sqlite3.connect(os.getenv("SQLITE_PATH")) as connection:
        with connection:
            cursor = connection.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            if cursor.fetchone() is None:
                connection.execute(
                    "INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,)
                )

