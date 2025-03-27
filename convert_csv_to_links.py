import csv
import json

# Read the CSV file
groups = {}
with open('forum_topics_with_links.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        topic_id = row['topic_id']
        groups[topic_id] = {
            "title": row['title'],
            "link": row['link'],
            "type": "Channel"
        }

# Add the main channel
groups["2399831251"] = {
    "title": "VOICES IGNITED MAIN",
    "link": "https://t.me/c/2399831251",
    "type": "Channel"
}

# Write to chat_links.json
with open('chat_links.json', 'w', encoding='utf-8') as f:
    json.dump(groups, f, indent=2)
