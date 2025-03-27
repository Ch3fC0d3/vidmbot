from telethon import TelegramClient
from telethon import TelegramClient
import csv
import time

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"  # Example: +123456789
from telethon import TelegramClient

# Replace with your actual API credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
PHONE_NUMBER = "your_phone_number"  # Example: +123456789

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_group_ids():
    await client.start(PHONE_NUMBER)
    dialogs = await client.get_dialogs()
    
    print("\n=== Group IDs ===")
    for dialog in dialogs:
        if dialog.is_group or dialog.is_channel:
            print(f"Name: {dialog.name}, ID: {dialog.entity.id}")

with client:
    client.loop.run_until_complete(get_group_ids())
