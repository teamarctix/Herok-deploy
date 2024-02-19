import asyncio
import logging
import time
import os
from importlib import import_module
from pyrogram import Client
from dotenv import load_dotenv
from config import API_ID, API_HASH, BOT_TOKEN

loop = asyncio.get_event_loop()
load_dotenv()
boot = time.time()

logging.basicConfig(
    handlers=[logging.FileHandler("Heroku-log.txt"), logging.StreamHandler()],
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)


Heroku = Client(
    ":heroku:",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

for file in os.listdir():
    if file.endswith(".session"):
        os.remove(file)
for file in os.listdir():
    if file.endswith(".session-journal"):
        os.remove(file)
#log_file_path = "Arctix-log.txt"
#if os.path.exists(log_file_path):
    #os.remove(log_file_path)
        

async def Heroku_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME
    await Heroku.start()
    getme = await Heroku.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name


loop.run_until_complete(Heroku_bot())