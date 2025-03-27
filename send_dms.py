from telethon import TelegramClient
import csv
import time
import asyncio
import logging
import json
import os
from datetime import datetime
from config import *

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_dm.log'),
        logging.StreamHandler()
    ]
)

# Create a backup of the members file
def create_backup():
    timestamp = int(time.time())
    backup_filename = f'members_backup_{timestamp}.csv'
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as original:
            with open(backup_filename, 'w', encoding='utf-8') as backup:
                backup.write(original.read())
        logging.info(f"Created backup: {backup_filename}")
        return backup_filename
    except Exception as e:
        logging.error(f"Failed to create backup: {str(e)}")
        return None

async def log_message_status(user_id, username, status, error=None):
    """Log message status to CSV file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if error:
            writer.writerow([timestamp, user_id, username, status, str(error)])
        else:
            writer.writerow([timestamp, user_id, username, status, ''])

async def log_failed_attempt(user_id, username, error):
    """Log failed attempts to a separate CSV file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(FAILED_ATTEMPTS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, user_id, username, str(error)])

# Save progress to resume later if needed
def save_progress(last_processed_index):
    progress = {"last_processed_index": last_processed_index}
    with open("dm_progress.json", "w") as f:
        json.dump(progress, f)
    logging.info(f"Progress saved: processed {last_processed_index} users")

# Load progress if exists
def load_progress():
    try:
        if os.path.exists("dm_progress.json"):
            with open("dm_progress.json", "r") as f:
                progress = json.load(f)
                return progress.get("last_processed_index", 0)
    except Exception as e:
        logging.error(f"Error loading progress: {str(e)}")
    return 0

async def send_messages():
    # Create backup before starting
    backup_file = create_backup()
    if not backup_file:
        logging.warning("Failed to create backup. Proceeding anyway...")
    
    # Create and start the client
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    # Initialize CSV files with headers if they don't exist
    for file_name, headers in [
        (LOG_FILE, ['Timestamp', 'User ID', 'Username', 'Status', 'Error']),
        (FAILED_ATTEMPTS_FILE, ['Timestamp', 'User ID', 'Username', 'Error'])
    ]:
        try:
            with open(file_name, 'x', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
        except FileExistsError:
            pass

    # Read the CSV file
    users = []
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                users.append(row)
    except FileNotFoundError:
        logging.error(f"Could not find input file: {CSV_FILE}")
        return
    
    total_users = len(users)
    logging.info(f'Found {total_users} users in CSV')
    
    # Load progress if we're resuming
    start_index = load_progress()
    if start_index > 0:
        logging.info(f"Resuming from user {start_index} of {total_users}")
    
    # Counter for tracking progress
    success_count = 0
    fail_count = 0
    skipped_count = 0
    
    # If in test mode, only send to test username
    if TEST_MODE:
        logging.info("Running in TEST MODE")
        users = [{'User ID': '7140127386', 'Username': TEST_USERNAME}]
        total_users = 1
        start_index = 0
    
    # Send messages
    for i, user in enumerate(users[start_index:], start=start_index):
        try:
            # Get user information
            user_id = None
            username = None
            
            # Try to get User ID from different possible column names
            if 'User ID' in user:
                user_id = user['User ID']
            elif 'user_id' in user:
                user_id = user['user_id']
            
            # Try to get Username from different possible column names
            if 'Username' in user:
                username = user['Username']
            elif 'username' in user:
                username = user['username']
            
            # Skip if no user ID
            if not user_id:
                skipped_count += 1
                logging.warning(f'Skipping user at index {i} with no User ID')
                continue
                
            # Log user info
            username_display = username if username and username != 'No Username' else 'No Username'
            logging.info(f'[{i+1}/{total_users}] Sending message to User ID: {user_id} (Username: {username_display})...')
            
            # Try to send message using User ID
            await client.send_message(int(user_id), MESSAGE_TEMPLATE)
            success_count += 1
            logging.info(f'Message sent to User ID: {user_id} successfully!')
            await log_message_status(user_id, username_display, 'SUCCESS')
            
            # Save progress every 10 users
            if i % 10 == 0:
                save_progress(i)
            
            # Wait between messages to avoid hitting rate limits
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)
            
        except Exception as e:
            fail_count += 1
            error_msg = str(e)
            logging.error(f'Failed to send message to User ID: {user_id}: {error_msg}')
            await log_message_status(user_id, username_display if 'username_display' in locals() else 'Unknown', 'FAILED', error_msg)
            await log_failed_attempt(user_id, username_display if 'username_display' in locals() else 'Unknown', error_msg)
            
            # Save progress after each failure
            save_progress(i)
            continue
    
    # Final progress save
    save_progress(total_users)
    
    logging.info(f'\nFinished sending messages!')
    logging.info(f'Successfully sent: {success_count}')
    logging.info(f'Failed: {fail_count}')
    logging.info(f'Skipped (no User ID): {skipped_count}')
    await client.disconnect()

# Run the async function
if __name__ == '__main__':
    try:
        asyncio.run(send_messages())
    except KeyboardInterrupt:
        logging.info("Script stopped by user")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
