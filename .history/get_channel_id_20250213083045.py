from telethon import TelegramClient
from telethon import TelegramClient
import csv
import time

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"  # Example: +123456789

from telethon import TelegramClient
import csv



# Replace with your group ID (Remember to add -100 before the ID)
GROUP_ID = -1002399831251

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_members():
    await client.start(PHONE_NUMBER)  # Authenticate if needed
    members = []
    
    async for user in client.iter_participants(GROUP_ID):
        username = user.username if user.username else "No Username"
        members.append([user.id, username, user.first_name, user.last_name])

    # Save members to CSV file
    with open("group_members.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "Username", "First Name", "Last Name"])
        writer.writerows(members)

    print(f"✅ Scraped {len(members)} members and saved them to 'group_members.csv'!")

with client:
    client.loop.run_until_complete(get_members())
