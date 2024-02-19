import os
from dotenv import load_dotenv
from os import getenv
load_dotenv()

API_ID = int(os.environ.get("API_ID", "11405252"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOGGER_ID = int(os.environ.get("LOGGER_ID"))
BOT_USERNAME = os.environ.get("BOT_USERNAME")
OWNER_ID = int(os.environ.get("OWNER_ID"))
EVALOP = list(map(int, getenv("EVALOP", "1881720028 5360305806").split()))
HEROKU_API = os.environ.get("HEROKU_API")
GIT_TOKEN = os.environ.get("GIT_TOKEN")