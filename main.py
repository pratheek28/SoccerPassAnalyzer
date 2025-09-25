import pandas as pd
import json
import requests


url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/18236.json"

events = requests.get(url).json()

passes = []

for event in events:
    if event['type']['name'] == 'Pass' and event['team']['name'] == 'Barcelona':
        passes.append({
            'player': event['player']['name'],
            'team': event['team']['name'],
            'minute': event['minute'],
            'second': event['second'],
            "x_start": event["location"][0],
            "y_start": event["location"][1],
            "x_end": event["pass"]["end_location"][0],
            "y_end": event["pass"]["end_location"][1],
            'outcome': event['pass']['outcome']['name'] if event['pass'].get('outcome') else 'Complete'
        })

df_passes = pd.DataFrame(passes)

print(df_passes.head())
