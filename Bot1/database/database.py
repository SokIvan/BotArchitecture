import json
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

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
    connection.close()
    
def persist_updates(update:list) -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_PATH"))
    with connection:

        connection.executemany(
            "INSERT INTO telegram_updates (payload) VALUES (?)",
            [(json.dumps(update, ensure_ascii=True, indent=2),)]
                               )
        
    connection.close()