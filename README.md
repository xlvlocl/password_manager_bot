# Password Manager Bot 🔒

***A telegram bot for secure password storage with end-to-end encryption.***

## 📌 Features

- ***Storing passwords in encrypted form***
- ***Complex password generator***
- ***Quick service search***
- ***Automatic deletion of messages***

## 🛠 Installing

***1. Clone repo:***
```bash
git clone https://github.com/xlvlocl/password_manager_bot.git
```
***2. Install requirements:***

```bash
pip install -r requirements.txt
```

***3. Create .env file and fill it:***

```ini
BOT_TOKEN=your_bot_token
ADMIN=ID_of_admin_1,ID_of_admin_2
KEY=your_fernet_key
```

***4. Run bot***

```bash
python run.py
```

## 🔐 Generating an encryption key
***To generate a new Fernet key, run once:***
```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```
## 📑 Generating database file
***To generate a new database, run once:***
```python
import os
import sqlite3


def main():
    db_path = "db/passwords.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS passwords 
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    encrypted_service BLOB NOT NULL,
    encrypted_username BLOB NOT NULL,
    encrypted_password BLOB NOT NULL,
    encrypted_notes BLOB 
    )
    """
        )

    conn.commit()
    conn.close()
    print("Done")


if __name__ == "__main__":
    main()
```


## ⚙️ Commands

| Command       |                                                               Description                                                                |
|:--------------|:----------------------------------------------------------------------------------------------------------------------------------------:|
| **/start**    |                                                _Help message_  <br/>_Usage:_<br/>`/start`                                                | 
| **/add**      |                            _Add new entry to database_<br/>_Usage:_ <br/>`/add <service> <login> <password>`                             |
| **/edit**     | _Edit existing entry_<br/>_Usage:_<br/>`/edit <sevice/ID> <field> <new_value>`<br/>_Available fields:_ `service, login, password, notes` |
| **/delete**   |                                      _Delete existing entry_<br/>_Usage:_<br/>`/delete <sevice/ID>`                                      |
| **/list**     |                                            _List of your passwords_<br/>_Usage:_<br/>`/list`                                             |
| **/password** |                                    _Generate password_<br/>_Usage:_<br/>`/password <len_of_password>`                                    |

## ⚠️ How check your password

***You should just type it's `service` or `ID` field in chat with bot, you can get `ID` in `/list` command***
