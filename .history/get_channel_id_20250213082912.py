from telethon import TelegramClient

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"  # Example: +123456789

from telethon import TelegramClient
import csv
import time



# Your message
MESSAGE = "Hello! We're reaching out to invite you to our new intake process. Let us know if you're interested!"

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def send_messages():
    await client.start(PHONE_NUMBER)

    with open("group_members.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            user_id = row[0]
            username = row[1]

            if username != "No Username":  # Only send to users with a username
                try:
                    await client.send_message(username, MESSAGE)
                    print(f"Message sent to {username}")
                    time.sleep(5)  # Delay to avoid rate limits
                except Exception as e:
                    print(f"Failed to send message to {username}: {e}")

with client:
    client.loop.run_until_complete(send_messages())
