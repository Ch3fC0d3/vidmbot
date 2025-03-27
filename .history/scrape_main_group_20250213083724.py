from telethon import TelegramClient
import csv

# Replace with your actual API credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
PHONE_NUMBER = "your_phone_number"

# Replace with the correct group ID (Use -100 before the ID)
GROUP_ID = -100XXXXXXXXXX  # Replace with actual group ID

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_members():
    await client.start(PHONE_NUMBER)  # Authenticate if needed
    members = []
    
    async for user in client.iter_participants(GROUP_ID):
        username = user.username if user.username else "No Username"
        phone = user.phone if user.phone else "No Phone"
        members.append([user.id, username, user.first_name, user.last_name, phone])

    # Save members to CSV file
    with open("group_members.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["User ID", "Username", "First Name", "Last Name", "Phone Number"])
        writer.writerows(members)

    print(f"✅ Scraped {len(members)} members and saved them to 'group_members.csv'!")

with client:
    client.loop.run_until_complete(get_members())
