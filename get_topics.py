from telethon import TelegramClient
from telethon.tl.functions.channels import GetForumTopicsRequest
import csv
from datetime import datetime

# Replace with your actual API credentials
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"

# VOICES IGNITED channel ID
CHANNEL_ID = -1002399831251

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

async def get_topics():
    await client.start(PHONE_NUMBER)
    
    print("🔄 Fetching forum topics...")
    
    try:
        # Get forum topics
        result = await client.get_entity(CHANNEL_ID)
        topics = await client(GetForumTopicsRequest(
            channel=result,
            offset_date=0,
            offset_id=0,
            offset_topic=0,
            limit=100
        ))

        # Prepare data for CSV
        topics_data = []
        for topic in topics.topics:
            topic_data = {
                'topic_id': topic.id,
                'title': topic.title,
                'created_date': datetime.fromtimestamp(topic.date.timestamp()).strftime('%Y-%m-%d %H:%M:%S'),
                'top_message': topic.top_message,
                'closed': getattr(topic, 'closed', False),
                'pinned': getattr(topic, 'pinned', False)
            }
            topics_data.append(topic_data)

        # Save to CSV
        with open('forum_topics.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['topic_id', 'title', 'created_date', 'top_message', 'closed', 'pinned'])
            writer.writeheader()
            writer.writerows(topics_data)

        print(f"✅ Successfully downloaded {len(topics_data)} topics to 'forum_topics.csv'!")
        
        # Print topics to console
        print("\nForum Topics:")
        for topic in topics_data:
            print(f"\nTitle: {topic['title']}")
            print(f"Created: {topic['created_date']}")
            print(f"ID: {topic['topic_id']}")
            print("-" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")

with client:
    client.loop.run_until_complete(get_topics())
