from telethon import TelegramClient
import csv
import asyncio
import logging
from config import API_ID, API_HASH, PHONE_NUMBER, MESSAGE_TEMPLATE

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_dm.log'),
        logging.StreamHandler()
    ]
)

async def test_send_message():
    # Create and start the client
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.start(PHONE_NUMBER)
    
    # Test user ID - using the CarTruck2 user ID from the CSV
    test_user_id = 7140127386
    
    try:
        logging.info(f"Attempting to send test message to user ID: {test_user_id}")
        
        # Try to send message using User ID
        await client.send_message(test_user_id, MESSAGE_TEMPLATE)
        logging.info(f"✅ Test message sent successfully to user ID: {test_user_id}")
        
    except Exception as e:
        logging.error(f"❌ Failed to send test message: {str(e)}")
    
    await client.disconnect()

# Run the async function
if __name__ == '__main__':
    try:
        asyncio.run(test_send_message())
        print("\nTest completed. Check test_dm.log for details.")
    except KeyboardInterrupt:
        print("Test stopped by user")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
