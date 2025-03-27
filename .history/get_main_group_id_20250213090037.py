from telethon import TelegramClient
from telethon import TelegramClient
import csv
import time

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"  # Example: +123456789

f
# Use the correct group ID (Add -100 before the ID)
GROUP_ID = -1002399831251  # Replace with your group ID

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_members():
    await client.start(PHONE_NUMBER)  # Authenticate if needed
    members = []
    
    print("🔄 Fetching members, please wait...")

    try:
        async for user in client.iter_participants(GROUP_ID, limit=None):
            username = user.username if user.username else "No Username"
            phone = user.phone if user.phone else "No Phone"
            members.append([user.id, username, user.first_name, user.last_name, phone])
            
            print(f"✅ Scraped: {user.first_name} {user.last_name} (@{username})")
            time.sleep(3)  # Longer delay to avoid rate limits

    except Exception as e:
        print(f"❌ Error: {e}")

    # Save members to CSV file
    with open("group_members_fixed.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "Username", "First Name", "Last Name", "Phone Number"])
        writer.writerows(members)

    print(f"✅ Successfully scraped {len(members)} members and saved them to 'group_members_fixed.csv'!")

with client:
    client.loop.run_until_complete(get_members())
