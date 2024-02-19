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


START_MESSAGE = "HEY, I AM A BOT"
START_BUTTONS = [
    [
         InlineKeyboardButton('MORE', callback_data="Test")
    ]
]

@app.on_message(
    filters.command("start")
    & filters.private
)
async def start_command(client, message):
    try:
        await message.reply_text(START_MESSAGE, reply_markup=InlineKeyboardMarkup(START_BUTTONS))
        
    except Exception as e:
        print(f"Error: {e}")
        
@app.on_callback_query()
async def callback_query(client, CallbackQuery):
    if CallbackQuery.data == "MORE":
        END_BUTTON = [
            [
                InlineKeyboardButton('MENU', callback_data="Go to Menu"),
                InlineKeyboardButton('MENU', callback_data="Go to Menu")
            ]
        ]
        CallbackQuery.edit_message_text(
            START_MESSAGE,
            reply_markup=InlineKeyboardMarkup(END_BUTTON)
        )
