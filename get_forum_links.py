import csv
import json
from datetime import datetime

# The main group ID where these forum topics are located
GROUP_ID = -1002399831251  # This is from your previous files

def create_forum_links(input_csv, output_csv):
    """Create t.me links for all forum topics"""
    topics = []
    
    # Read the input CSV
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create the t.me link for the forum topic
            # Format: https://t.me/c/XXXXX/YYYY where XXXXX is group ID without -100 and YYYY is topic ID
            group_id_str = str(abs(GROUP_ID))[3:]  # Remove -100 from the start
            topic_link = f"https://t.me/c/{group_id_str}/{row['topic_id']}"
            
            # Add link to the row data
            row['link'] = topic_link
            topics.append(row)
    
    # Write to new CSV with links
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['topic_id', 'title', 'created_date', 'top_message', 'closed', 'pinned', 'link']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(topics)
    
    # Also save as JSON for easy programmatic access
    with open('forum_topics_with_links.json', 'w', encoding='utf-8') as f:
        json.dump(topics, f, indent=2)
    
    return topics

def print_topics(topics):
    """Print topics in an organized way"""
    print("\n📱 Forum Topics and Links:")
    
    # First print pinned topics
    print("\n📌 PINNED TOPICS:")
    for topic in topics:
        if topic['pinned'].lower() == 'true':
            print(f"\n{topic['title']}")
            print(f"Link: {topic['link']}")
            print(f"Created: {topic['created_date']}")
            print(f"Status: {'🔒 Closed' if topic['closed'].lower() == 'true' else '🔓 Open'}")
    
    # Then print state/location topics
    print("\n🗺️ STATE/LOCATION TOPICS:")
    state_topics = [t for t in topics if t['pinned'].lower() != 'true' and t['title'].split(',')[0] in [
        'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 
        'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
        'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
        'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
        'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
        'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
        'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
        'Wisconsin', 'Wyoming', 'DC'
    ]]
    for topic in state_topics:
        print(f"\n{topic['title']}")
        print(f"Link: {topic['link']}")
    
    # Then print other topics
    print("\n📑 OTHER TOPICS:")
    other_topics = [t for t in topics if t['pinned'].lower() != 'true' and t not in state_topics]
    for topic in other_topics:
        print(f"\n{topic['title']}")
        print(f"Link: {topic['link']}")
        print(f"Created: {topic['created_date']}")

if __name__ == "__main__":
    input_file = 'forum_topics.csv'
    output_file = 'forum_topics_with_links.csv'
    
    print("🔍 Generating links for forum topics...")
    topics = create_forum_links(input_file, output_file)
    
    print(f"✅ Generated links for {len(topics)} topics!")
    print(f"📊 Results saved to '{output_file}' and 'forum_topics_with_links.json'")
    
    print_topics(topics)
