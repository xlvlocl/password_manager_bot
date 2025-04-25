from src.config import logger
import os
import sqlite3
from cryptography.fernet import Fernet


logger = logger.get_logger(__name__)


def main():
    db_path = "db/passwords.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encrypted_service BLOB NOT NULL,
    encrypted_username BLOB NOT NULL,
    encrypted_password BLOB NOT NULL,
    encrypted_notes BLOB )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Passwords database created")

    key = Fernet.generate_key().decode()

    env_content = \
    f"""
    BOT_TOKEN=your_bot_token
    ADMIN=your_telegram_id,another_telegram_id
    KEY={key}
    """

    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    logger.info("✅ Key generated")


main()
