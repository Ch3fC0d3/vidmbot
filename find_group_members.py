from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import csv
import os
from config import API_ID, API_HASH
import time
import string
from datetime import datetime

def get_output_filename():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f'members_{timestamp}.csv'

def save_member(member_info, filename):
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['User ID', 'Username', 'First Name', 'Last Name', 'Group ID', 'Group Title'])
        writer.writerow([
            member_info['User ID'],
            member_info['Username'],
            member_info['First Name'],
            member_info['Last Name'],
            member_info['Group ID'],
            member_info['Group Title']
        ])

def main():
    output_file = get_output_filename()
    print(f"Will save members to: {output_file}")
    
    with TelegramClient('anon', API_ID, API_HASH) as client:
        print("Connected to Telegram")
        
        channel = client.get_entity(-1002399831251)
        print(f"Connected to channel: {channel.title}")
        
        total_members = 0
        search_letters = list(string.ascii_lowercase) + list(string.digits) + ['_']
        
        for letter in search_letters:
            try:
                offset = 0
                has_more = True
                
                while has_more:
                    participants = client(GetParticipantsRequest(
                        channel=channel,
                        filter=ChannelParticipantsSearch(letter),
                        offset=offset,
                        limit=200,
                        hash=0
                    ))
                    
                    if not participants.users:
                        break
                        
                    for user in participants.users:
                        if not user.bot and not user.deleted and not user.fake:
                            member_info = {
                                'User ID': str(user.id),
                                'Username': user.username if user.username else 'No Username',
                                'First Name': user.first_name if user.first_name else '',
                                'Last Name': user.last_name if user.last_name else '',
                                'Group ID': str(channel.id),
                                'Group Title': channel.title
                            }
                            save_member(member_info, output_file)
                            total_members += 1
                            print(f"\rTotal members saved: {total_members} (Current letter: {letter})", end='')
                    
                    offset += len(participants.users)
                    has_more = len(participants.users) == 200
                    
            except Exception as e:
                print(f"\nError with letter {letter}: {str(e)}")
                time.sleep(2)
                continue
                
        print(f"\nFinished! Total members saved: {total_members}")
        print(f"Members saved to: {output_file}")

if __name__ == '__main__':
    main()