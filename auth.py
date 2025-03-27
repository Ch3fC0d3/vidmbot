from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER
import os

async def main():
    print("Starting authentication...")
    
    # Remove the old session file if it exists
    session_file = 'anon.session'
    if os.path.exists(session_file):
        try:
            os.remove(session_file)
            print("Removed old session file")
        except Exception as e:
            print(f"Error removing old session: {str(e)}")
    
    client = TelegramClient('anon', API_ID, API_HASH)
    
    await client.connect()
    
    if not await client.is_user_authorized():
        print("\nSending code request...")
        await client.send_code_request(PHONE_NUMBER)
        
        try:
            print("\nPlease check your Telegram app for the verification code")
            code = input("Enter the code: ")
            await client.sign_in(PHONE_NUMBER, code)
            print("\nSuccessfully authenticated!")
            
        except Exception as e:
            print(f"\nError during authentication: {str(e)}")
    else:
        print("Already authenticated!")
        
    await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
