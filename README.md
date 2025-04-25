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

***3. Run:***
```bash
python setup.py
```

***4. Add data in .env:***
- ***BOT_TOKEN - Your Telegram bot token***
- ***ADMIN - Your ID in Telegram***

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
