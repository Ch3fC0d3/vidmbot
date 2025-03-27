from telethon import TelegramClient
import csv
import json

# Your Telegram API credentials
API_ID = '25511416'
API_HASH = '2f4e466bfe882f3e9322b9d0f8d58dbb'
PHONE_NUMBER = '+16462839825'

async def get_chat_links(client):
    """Get chat IDs and their corresponding t.me links"""
    chat_links = {}
    
    # Get dialogs (chats/channels/groups)
    async for dialog in client.iter_dialogs():
        chat_id = dialog.id
        entity = dialog.entity
        
        # Create t.me link if possible
        if hasattr(entity, 'username') and entity.username:
            link = f"https://t.me/{entity.username}"
        else:
            # For private chats/groups, we can use invite links if available
            try:
                invite_link = await client.get_entity(chat_id)
                if hasattr(invite_link, 'invite_link') and invite_link.invite_link:
                    link = invite_link.invite_link
                else:
                    link = f"Private chat (ID: {chat_id})"
            except:
                link = f"Private chat (ID: {chat_id})"
        
        chat_links[chat_id] = {
            'title': dialog.title,
            'link': link,
            'type': str(type(entity).__name__)
        }
    
    return chat_links

async def export_chat_links():
    """Export all chat links to both CSV and JSON formats"""
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    chat_links = await get_chat_links(client)
    
    # Export to CSV
    with open('chat_links.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Chat ID', 'Title', 'Link', 'Type'])
        for chat_id, info in chat_links.items():
            writer.writerow([chat_id, info['title'], info['link'], info['type']])
    
    # Export to JSON for easier programmatic access
    with open('chat_links.json', 'w', encoding='utf-8') as f:
        json.dump(chat_links, f, indent=2)
    
    print(f"✅ Exported {len(chat_links)} chat links to 'chat_links.csv' and 'chat_links.json'")
    return chat_links

def get_chat_link(chat_id, json_file='chat_links.json'):
    """Get a chat link from the saved JSON file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            chat_links = json.load(f)
        return chat_links.get(str(chat_id))
    except FileNotFoundError:
        return None

if __name__ == "__main__":
    # Run the export function
    import asyncio
    asyncio.run(export_chat_links())
