import os
import time
import requests
from pyrogram.types import Message
from pyrogram import Client, filters
from heroku3 import from_key
from Heroku import Heroku as app
from config import OWNER_ID, HEROKU_API
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_MESSAGE = "HEY, I AM A BOT"
LOGIN_MESSAGE = "By tapping on the link , you can get the Heroku Api key 🗝️"
LOGIN_MESSAGE_BUTTONS = [
    [InlineKeyboardButton('Generate Heroku Api Token', url='https://dashboard.heroku.com/account/applications/authorizations/new')]
]

@app.on_message(
    filters.command("login")
    & filters.private
)
def link(client, message):
    text = LOGIN_MESSAGE
    reply_markup = InlineKeyboardMarkup(LOGIN_MESSAGE_BUTTONS)
    # Send the message with text and reply_markup
    message.reply_text(text, reply_markup=reply_markup)

# @app.on_message(
    # filters.command("start")
    # & filters.private
# )
# async def start_command(client, message):
    # try:
        # await message.reply_text("Hi! This is a reply message.")
        # print("Command executed successfully.")
    # except Exception as e:
        # print(f"Error: {e}")


# Command to save API key to a temporary file
@app.on_message(
    filters.command("api")
    & filters.private
)
def api_command(client, message):
    # Extracting the API key from the command
    api_key = message.text.split(" ", 1)[1].strip()

    # Save the API key with the user's ID to a temporary file
    user_id = message.from_user.id
    file_name = f"temp_api_key_{user_id}.txt"
    
    with open(file_name, "w") as file:
        file.write(api_key)

    # Respond to the user
    message.reply_text(f"API key '{api_key}' has been saved to a temporary file for user {user_id}.")

@app.on_message(
    filters.command("auth")
    & filters.private
)
def auth_command(client, message):
    # Check if the user has saved an API key
    user_id = message.from_user.id
    file_name = f"temp_api_key_{user_id}.txt"
    
    if os.path.exists(file_name):
        # User has saved an API key
        message.reply_text("You have already saved an API key.")
    else:
        # User has not saved an API key, provide buttons
        reply_markup = InlineKeyboardMarkup(LOGIN_MESSAGE_BUTTONS)
        message.reply_text("You haven't saved an API key. Please use the /api command to save one.", reply_markup=reply_markup)
        
# @app.on_message(
    # filters.command("login")
    # & filters.private
   # )
# async def login_command(client, message):
    # try:
          