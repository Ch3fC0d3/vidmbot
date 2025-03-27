from telethon import TelegramClient, errors
import time
from chat_utils import get_chat_link
import os
import random
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sent_messages():
    sent_messages = set()
    if os.path.exists('sent_messages.txt'):
        with open('sent_messages.txt', 'r') as f:
            for line in f:
                sent_messages.add(line.strip())
    return sent_messages

def save_sent_message(username):
    with open('sent_messages.txt', 'a') as f:
        f.write(f"{username}\n")

def get_random_delay(min_delay=2, max_delay=6):
    """Get a random delay between min and max seconds"""
    return random.uniform(min_delay, max_delay)

async def send_message_with_retry(client, username, message, max_retries=3):
    """Send message with retry logic"""
    for attempt in range(max_retries):
        try:
            await client.send_message(username, message)
            logger.info(f"Message sent to @{username}")
            return True
        except errors.FloodWaitError as e:
            logger.warning(f"Flood wait error. Waiting for {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
        except errors.RPCError as e:
            if "Too many requests" in str(e):
                logger.warning(f"Rate limit hit. Waiting for longer...")
                await asyncio.sleep(30)  # Reduced wait time
            else:
                logger.error(f"Error sending message to @{username}: {e}")
                return False
        except Exception as e:
            logger.error(f"Unexpected error sending message to @{username}: {e}")
            return False
        
        if attempt < max_retries - 1:
            wait_time = get_random_delay(0.5, 2)
            logger.info(f"Retrying in {wait_time:.1f} seconds...")
            await asyncio.sleep(wait_time)
    return False

async def process_batch(client, usernames, message, batch_size=10):
    """Process a batch of usernames with parallel processing"""
    tasks = []
    for username in usernames:
        tasks.append(send_message_with_retry(client, username, message))
    
    # Process tasks in parallel with a limit
    semaphore = asyncio.Semaphore(5)  # Limit concurrent tasks
    
    async def limited_task(task):
        async with semaphore:
            return await task
    
    limited_tasks = [limited_task(task) for task in tasks]
    results = await asyncio.gather(*limited_tasks, return_exceptions=True)
    
    # Add random delay between batches
    delay = get_random_delay(3, 7)
    logger.info(f"Completed batch. Waiting {delay:.1f} seconds before next batch...")
    await asyncio.sleep(delay)
    
    return results

async def send_messages():
    await client.start(PHONE_NUMBER)  # Authenticate if needed
    
    # Load previously sent messages
    sent_messages = load_sent_messages()
    
    # Get the channel entity to get its ID
    channel = await client.get_entity(CHANNEL_USERNAME)
    channel_info = get_chat_link(channel.id)
    if channel_info:
        logger.info(f"Sending messages to members of: {channel_info['title']}")
        logger.info(f"Channel link: {channel_info['link']}")
    
    # Collect all usernames first
    usernames = []
    async for user in client.iter_participants(CHANNEL_USERNAME):
        if user.username and user.username not in sent_messages:
            usernames.append(user.username)
    
    total_users = len(usernames)
    logger.info(f"Total users to message: {total_users}")
    
    # Split into chunks for parallel processing
    chunk_size = 50  # Process 50 users at a time
    chunks = [usernames[i:i + chunk_size] for i in range(0, total_users, chunk_size)]
    
    # Process chunks in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        loop = asyncio.get_event_loop()
        futures = []
        
        for chunk in chunks:
            future = loop.run_in_executor(
                executor,
                lambda: asyncio.run(process_batch(client, chunk, MESSAGE))
            )
            futures.append(future)
        
        # Wait for all futures to complete
        for future in futures:
            try:
                results = await future
                for result in results:
                    if result:
                        save_sent_message(usernames[0])  # Save only successful sends
                        usernames.pop(0)
            except Exception as e:
                logger.error(f"Error processing chunk: {e}")
    
    logger.info("Message sending completed!")

# Your Telegram API credentials (replace with yours)
API_ID = '25511416'
API_HASH = '2f4e466bfe882f3e9322b9d0f8d58dbb'
PHONE_NUMBER = '+16462839825'  # Example: +123456789

# Replace with your channel username (without @)
CHANNEL_USERNAME = 'your_channel_username_here'

# Your message
MESSAGE = """Hey You! 

We've missed you! We're gearing up for some exciting events starting this weekend, and we'd love for you to be a part of it. It's time to come back together, take action, and make an impact.

Check out the details and reach out. We need your energy and ideas now more than ever!

Let's do this! 

You can connect with us here: t.me/VIPlacement_bot or https://t.me/+cVFRbC9KYHJmZTQx"""

# Create a Telegram client session
client = TelegramClient('session_name', API_ID, API_HASH)

with client:
    client.loop.run_until_complete(send_messages())
