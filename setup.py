import shutil
import stat

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

    files_to_remove = [
        "README.md",
        ".gitignore",
        "requirements.txt",
        "setup.py"
        ]

    git_dir = ".git"
    if os.path.exists(git_dir):
        try:
            for root, dirs, files in os.walk(git_dir):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    os.chmod(dir_path, stat.S_IWRITE | stat.S_IREAD | stat.S_IEXEC)
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    os.chmod(file_path, stat.S_IWRITE | stat.S_IREAD)
            shutil.rmtree(git_dir)
            logger.info(f"✅ Folder {git_dir} removed.")
        except Exception as e:
            logger.warning(f"❌ Cannot remove folder {git_dir}.")
    else:
        logger.warning(f"❌ Folder {git_dir} not found.")

    for file in files_to_remove:
        try:
            os.remove(file)
            logger.info(f"✅ File {file} removed.")
        except:
            logger.warning(f"❌ Cannot remove file {file}.")


main()
