print("Test script starting...")
import pandas as pd
print("Pandas imported successfully")
df = pd.read_csv('forum_topics_with_links.csv')
print(f"Found {len(df)} topics in CSV")
print("Test script finished!")
