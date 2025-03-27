from telethon import TelegramClient

# Replace with your credentials
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE_NUMBER = 'YOUR_PHONE_NUMBER'

async def get_channels_from_group():
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        await client.start(PHONE_NUMBER)
        dialogs = await client.get_dialogs()

        print("Channels in Groups:")
        for dialog in dialogs:
            if dialog.is_group and dialog.is_channel:
                print(f"Channel: {dialog.name}, ID: {dialog.entity.id}")

# Run the script
import asyncio
asyncio.run(get_channels_from_group())
