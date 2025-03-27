from telethon import TelegramClient
import time

# Your Telegram API credentials (replace with yours)
API_ID = 'your_api_id_here'
API_HASH = 'your_api_hash_here'
PHONE_NUMBER = 'your_phone_number_here'  # Example: +123456789

# Replace with your channel username (without @)
CHANNEL_USERNAME = 'your_channel_username_here'

# Your message
MESSAGE = "We're looking for members to try out our new intake process! Let us know if you're interested."

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def send_messages():
    await client.start(PHONE_NUMBER)  # Authenticate if needed
    async for user in client.iter_participants(CHANNEL_USERNAME):
        if user.username:  # Only send messages to users with a public username
            try:
                await client.send_message(user.username, MESSAGE)
                print(f"Message sent to {user.username}")
                time.sleep(5)  # Delay to avoid rate limits
            except Exception as e:
                print(f"Failed to send message to {user.username}: {e}")

with client:
    client.loop.run_until_complete(send_messages())
