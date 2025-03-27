# Telegram DM Bot

This bot allows you to send direct messages to a list of Telegram users from a CSV file.

## Setup Instructions

1. First, you need to get your Telegram API credentials:
   - Go to https://my.telegram.org/auth
   - Log in with your phone number
   - Go to 'API development tools'
   - Create a new application
   - Copy your API ID and API Hash

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file:
   - Copy .env.example to .env
   - Fill in your API_ID, API_HASH, and PHONE number
   - Add your message template in the MESSAGE variable

4. Run the script:
   ```bash
   python send_dms.py
   ```

## Important Notes

- The script includes a 30-second delay between messages to avoid hitting Telegram's rate limits
- Users without usernames will be skipped
- The script will create a session file on first run - you'll need to enter the verification code sent to your Telegram
- Be careful with mass messaging as it could lead to account restrictions if abused
