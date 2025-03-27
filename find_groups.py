from telethon import TelegramClient
from telethon.tl.types import Channel, Chat, User

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def find_groups():
    await client.start(PHONE_NUMBER)
    
    print("🔄 Fetching all dialogs (chats and groups)...")
    
    try:
        async for dialog in client.iter_dialogs():
            # Check if it's a group or channel
            if isinstance(dialog.entity, (Channel, Chat)):
                print(f"Title: {dialog.name}")
                print(f"ID: {dialog.id}")
                print(f"Type: {'Channel' if isinstance(dialog.entity, Channel) else 'Group'}")
                print(f"Members: {dialog.entity.participants_count if hasattr(dialog.entity, 'participants_count') else 'Unknown'}")
                print("-" * 50)
                
    except Exception as e:
        print(f"❌ Error: {e}")

    print("✅ Finished fetching all groups and channels!")

with client:
    client.loop.run_until_complete(find_groups())
