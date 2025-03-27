from telethon import TelegramClient
import csv
import json
import re

# Your Telegram API credentials
API_ID = '25511416'
API_HASH = '2f4e466bfe882f3e9322b9d0f8d58dbb'
PHONE_NUMBER = '+16462839825'

async def get_voices_ignited_chats(client):
    """Get all chats related to Voices Ignited"""
    voices_chats = {}
    
    # Keywords to identify Voices Ignited related groups
    keywords = ['voices', 'ignited', 'vi', 'mayday', 'may day', 'voice']
    
    async for dialog in client.iter_dialogs():
        title = dialog.title.lower()
        # Check if any keyword matches
        if any(keyword in title for keyword in keywords):
            chat_id = dialog.id
            entity = dialog.entity
            
            # Get chat link
            if hasattr(entity, 'username') and entity.username:
                link = f"https://t.me/{entity.username}"
            else:
                try:
                    invite_link = await client.get_entity(chat_id)
                    if hasattr(invite_link, 'invite_link') and invite_link.invite_link:
                        link = invite_link.invite_link
                    else:
                        link = f"Private chat (ID: {chat_id})"
                except:
                    link = f"Private chat (ID: {chat_id})"
            
            # Get member count
            try:
                full_chat = await client.get_entity(chat_id)
                if hasattr(full_chat, 'participants_count'):
                    member_count = full_chat.participants_count
                else:
                    member_count = 'Unknown'
            except:
                member_count = 'Unknown'
            
            voices_chats[chat_id] = {
                'title': dialog.title,
                'link': link,
                'type': str(type(entity).__name__),
                'members': member_count
            }
    
    return voices_chats

async def export_voices_ignited_chats():
    """Export all Voices Ignited related chats to CSV and JSON"""
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    print("🔍 Finding Voices Ignited related chats...")
    chat_links = await get_voices_ignited_chats(client)
    
    # Export to CSV
    with open('voices_ignited_chats.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Chat ID', 'Title', 'Link', 'Type', 'Member Count'])
        for chat_id, info in chat_links.items():
            writer.writerow([chat_id, info['title'], info['link'], info['type'], info['members']])
    
    # Export to JSON
    with open('voices_ignited_chats.json', 'w', encoding='utf-8') as f:
        json.dump(chat_links, f, indent=2)
    
    print(f"✅ Found {len(chat_links)} Voices Ignited related chats!")
    print("📊 Results exported to 'voices_ignited_chats.csv' and 'voices_ignited_chats.json'")
    
    # Print the results
    print("\n📱 Chat Links:")
    for chat_id, info in chat_links.items():
        print(f"\n{info['title']}")
        print(f"Link: {info['link']}")
        print(f"Type: {info['type']}")
        print(f"Members: {info['members']}")
    
    await client.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(export_voices_ignited_chats())
