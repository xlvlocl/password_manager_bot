import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN").split(",")))
KEY = os.getenv("KEY")
