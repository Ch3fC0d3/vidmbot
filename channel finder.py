from telethon import TelegramClient

API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"

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
