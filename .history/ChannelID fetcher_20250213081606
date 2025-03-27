from telethon import TelegramClient

# Replace with your actual API credentials
API_ID = "your_api_id"
API_HASH = "your_api_hash"
PHONE_NUMBER = "your_phone_number"  # Example: +123456789

# Create a client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    async with client:
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            print(f"Name: {dialog.name}, ID: {dialog.entity.id}")

with client:
    client.loop.run_until_complete(main())
