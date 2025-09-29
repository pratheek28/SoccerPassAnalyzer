import pandas as pd
import json
import requests
import matplotlib.pyplot as plt
import networkx as nx

#UCL 2010/2011 Final
url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/18236.json"

# UCL 2014/15 Final
#url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/18242.json"
events = requests.get(url).json()


def drawPitch(ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 7))

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, 80], color="black")
    plt.plot([0, 120], [80, 80], color="black")
    plt.plot([120, 120], [80, 0], color="black")
    plt.plot([120, 0], [0, 0], color="black")
    plt.plot([60, 60], [0, 80], color="black")

    # Left Penalty Area
    plt.plot([18, 18], [62, 18], color="black")
    plt.plot([0, 18], [62, 62], color="black")
    plt.plot([0, 18], [18, 18], color="black")

    # Right Penalty Area
    plt.plot([102, 102], [62, 18], color="black")
    plt.plot([120, 102], [62, 62], color="black")
    plt.plot([120, 102], [18, 18], color="black")

    # Center Circle
    centreCircle = plt.Circle((60, 40), 10, color="black", fill=False)
    ax.add_patch(centreCircle)

    ax.axis('off')
    return ax



passes = []
for event in events:
    if event['type']['name'] == 'Pass' and event['team']['name'] == 'Barcelona' and event['minute'] <= 120:
        passes.append({
            'player': event['player']['name'],
            'receiver': event['pass']['recipient']['name'] if event['pass'].get('recipient') else None,
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

# Group by 'player'
avgPosition = df_passes.groupby('player').agg({
    'x_start': 'mean',
    'y_start': 'mean'
})

# Build passing network
G = nx.DiGraph()
for _, row in df_passes.iterrows():
    if row['outcome'] == 'Complete' and row['receiver'] is not None:
        if G.has_edge(row['player'], row['receiver']):
            G[row['player']][row['receiver']]['weight'] += 1
        else:
            G.add_edge(row['player'], row['receiver'], weight=1)

# Draw pitch + average positions
fig, ax = plt.subplots(figsize=(12, 8))
drawPitch(ax)

for player, row in avgPosition.iterrows():
    ax.scatter(row['x_start'], row['y_start'], s=300, color='skyblue', edgecolors='black', marker='o')
    ax.text(row['x_start'], row['y_start'], player, fontsize=10, ha='center', va='center')

# Draw arrows between players
for (p1, p2, data) in G.edges(data=True):
    if p1 in avgPosition.index and p2 in avgPosition.index:
        x1, y1 = avgPosition.loc[p1]
        x2, y2 = avgPosition.loc[p2]
        ax.annotate("",
            xy=(x2, y2), xycoords="data",
            xytext=(x1, y1), textcoords="data",
            arrowprops=dict(arrowstyle="->", lw=data["weight"]*0.3, color="gray")
        )

plt.show()
