from telethon import TelegramClient
import csv
import time
import asyncio

# API credentials from scrape_fixed.py
API_ID = "25511416"
API_HASH = "2f4e466bfe882f3e9322b9d0f8d58dbb"
PHONE_NUMBER = "+16462839825"

# Message template - customize this
MESSAGE_TEMPLATE = """
We're looking for people to try out our new member intake process! This will help speed up future onboarding while also allowing us to match you with the best groups for your skills and interests! Follow the link @May_Day2_Bot  




"""

async def send_messages():
    # Create and start the client
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    # Read the CSV file
    users = []
    with open('group_members_fixed.csv', 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            users.append(row)
    
    print(f'Found {len(users)} users in CSV')
    
    # Counter for tracking progress
    success_count = 0
    fail_count = 0
    
    # Send messages
    for user in users:
        try:
            username = user['Username']
            if username == 'No Username':
                print(f'Skipping user with no username')
                continue
                
            print(f'Sending message to {username}...')
            
            # Try to send message
            await client.send_message(username, MESSAGE_TEMPLATE)
            success_count += 1
            print(f' Message sent to {username} successfully!')
            
            # Wait between messages to avoid hitting rate limits
            await asyncio.sleep(30)  # 30 second delay between messages
            
        except Exception as e:
            fail_count += 1
            print(f' Failed to send message to {username}: {str(e)}')
            continue
    
    print(f'\nFinished sending messages!')
    print(f'Successfully sent: {success_count}')
    print(f'Failed: {fail_count}')
    await client.disconnect()

# Run the async function
if __name__ == '__main__':
    asyncio.run(send_messages())
