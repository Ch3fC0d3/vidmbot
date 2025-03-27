from telethon import TelegramClient
import time

# Your Telegram API credentials (replace with yours)
API_ID = '25511416'
API_HASH = '2f4e466bfe882f3e9322b9d0f8d58dbb'
PHONE_NUMBER = '+16462839825'  # Example: +123456789

# Replace with your channel username (without @)
CHANNEL_USERNAME = 'your_channel_username_here'

# Your message
MESSAGE = "We're looking for people to try out our new member intake process! This will help speed up future onboarding while also allowing us to match you with the best groups for your skills and interests! Follow the link @May_Day2_Bot"

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
