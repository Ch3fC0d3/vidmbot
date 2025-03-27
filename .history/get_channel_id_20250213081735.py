from telethon import TelegramClient

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"  # Example: +123456789

# Create a client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def main():
    async with client:
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            print(f"Name: {dialog.name}, ID: {dialog.entity.id}")

with client:
    client.loop.run_until_complete(main())
