import os
import time
import requests
from pyrogram.types import Message
from pyrogram import Client, filters
from heroku3 import from_key
from Heroku import Heroku as app
from config import OWNER_ID, HEROKU_API
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# MongoDB connection setup
mongo_client = MongoClient("mongodb+srv://abcd:abcd@personalproject.mxx6dgi.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["arctix"]
collection = db["api_keys"]

START_MESSAGE = "HEY, I AM A BOT"
START_MESSAGE_BUTTONS = [
    [InlineKeyboardButton('CHANNEL', url='https://youtu.be/W6GNvbwhsyY?si=E6DqauakwzWKkI9B')]
]

# Command to save API key with the user's ID to MongoDB
@app.on_message(
    filters.command("mapi")
    & filters.private
)
def api_command(client, message):
    # Extracting the API key from the command
    api_key = message.text.split(" ", 1)[1].strip()

    # Save the API key with the user's ID to MongoDB
    user_id = message.from_user.id
    collection.update_one({"user_id": user_id}, {"$set": {"api_key": api_key}}, upsert=True)

    # Respond to the user
    message.reply_text(f"API key '{api_key}' has been saved to MongoDB for user {user_id}.")

# Command to check if the user has saved an API key in MongoDB and provide buttons if not
@app.on_message(
    filters.command("mauth")
    & filters.private
)
def auth_command(client, message):
    # Check if the user has saved an API key in MongoDB
    user_id = message.from_user.id
    api_record = collection.find_one({"user_id": user_id})
    
    if api_record:
        # User has saved an API key
        message.reply_text(f"You have already saved an API key: {api_record['api_key']}.")
    else:
        # User has not saved an API key, provide buttons
        reply_markup = InlineKeyboardMarkup(START_MESSAGE_BUTTONS)
        message.reply_text("You haven't saved an API key. Please use the /api command to save one.", reply_markup=reply_markup)

# Command to display the start message
@app.on_message(
    filters.command("mstart")
    & filters.private
)
async def start_command(client, message):
    try:
        await message.reply_text("Hi! This is a reply message.")
        print("Command executed successfully.")
    except Exception as e:
        print(f"Error: {e}")


# Command to remove the stored API key for the user from MongoDB
@app.on_message(
    filters.command("rmauth")
    & filters.private
)
def rmauth_command(client, message):
    # Remove the stored API key for the user from MongoDB
    user_id = message.from_user.id
    result = collection.delete_one({"user_id": user_id})

    if result.deleted_count > 0:
        message.reply_text("Your stored API key has been removed.")
    else:
        message.reply_text("No stored API key found for removal.")        
        
# Function to fetch Heroku API information
def get_heroku_info(api_key):
    heroku = from_key(api_key)
    email = heroku.account().email()
    apps = [app.name for app in heroku.apps()]

    return email, apps

# Function to handle incoming messages and fetch Heroku API information
@app.on_message(filters.private)
def handle_messages(client, message):
    user_id = message.from_user.id

    # Check if the user has a stored API key
    api_record = collection.find_one({"user_id": user_id})
    
    if api_record:
        # Extract potential Heroku API key from the incoming message
        potential_api_key = message.text.strip()

        # Check if the potential_api_key is a valid Heroku API key
        if len(potential_api_key) == 40 and potential_api_key.isalnum():
            # Fetch Heroku API information
            email, apps = get_heroku_info(potential_api_key)

            # Respond to the user with extracted information
            response_text = f"Email: {email}\nApps: {', '.join(apps)}"
            message.reply_text(response_text)
        else:
            message.reply_text("No valid Heroku API key found in the message.")
    else:
        message.reply_text("You haven't saved an API key. Please use the /api command to save one.")
                
        
        
        
        
        
        
        
        