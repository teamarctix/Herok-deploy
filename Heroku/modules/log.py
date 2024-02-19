from pyrogram import Client, filters
from Heroku import Heroku as app
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
import os
import requests

def paste_to_spacebin(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        file_extension = file_path.split('.')[-1]
        response = requests.post('https://spaceb.in/api/v1/documents', data={'content': content, 'extension': file_extension})

        if response.status_code == 201:
            document_id = response.json().get('payload', {}).get('id')
            return f'https://spaceb.in/{document_id}'
        else:
            return f"Error: {response.json().get('error')}"

    except Exception as e:
        return f"Error: {e}"

@app.on_message(filters.command("log") & filters.private & filters.user(OWNER_ID))
async def log_command(client: Client, message: Message):
    log_file_path = "Heroku-log.txt"
    
    if os.path.exists(log_file_path):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Web View", url=paste_to_spacebin(log_file_path))]
        ])
        
        await client.send_document(message.chat.id, document=log_file_path, reply_markup=keyboard)
    else:
        await message.reply("Log file not found.")