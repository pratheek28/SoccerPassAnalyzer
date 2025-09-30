import pandas as pd
import json
import requests
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons
import networkx as nx

#UCL 2010/2011 Final
url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/18236.json"

# UCL 2014/15 Final
#url = "https://raw.githubusercontent.com/statsbomb/open-data/refs/heads/master/data/events/18242.json"


events = requests.get(url).json()


def buttonClick(value):
    plt.close()
    showPassNetwork(value)
    

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



def showPassNetwork(time):
    passes = []
    for event in events:
        if event['type']['name'] == 'Pass' and event['team']['name'] == 'Barcelona' and event['minute'] <= time:
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

    # Group by player to get average positions
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

    # Shows passes for the first 10, 20, 30, 60, 75, and 90 minutes of the game, as well as the full game (if the game went into extra time)!
    buttonAxis10 = plt.axes([0.1, 0.05, 0.1, 0.04])
    btn10 = Button(buttonAxis10, '10', color='lightgoldenrodyellow', hovercolor='0.975')
    btn10.on_clicked(lambda event: buttonClick(10))

    buttonAxis20 = plt.axes([0.21, 0.05, 0.1, 0.04])
    btn20 = Button(buttonAxis20, '20', color='lightgoldenrodyellow', hovercolor='0.975')
    btn20.on_clicked(lambda event: buttonClick(20))

    buttonAxis30 = plt.axes([0.32, 0.05, 0.1, 0.04])
    btn30 = Button(buttonAxis30, '30', color='lightgoldenrodyellow', hovercolor='0.975')
    btn30.on_clicked(lambda event: buttonClick(30))

    buttonAxis45 = plt.axes([0.43, 0.05, 0.1, 0.04])
    btn45 = Button(buttonAxis45, '45', color='lightgoldenrodyellow', hovercolor='0.975')
    btn45.on_clicked(lambda event: buttonClick(45))

    buttonAxis60 = plt.axes([0.54, 0.05, 0.1, 0.04])
    btn60 = Button(buttonAxis60, '60', color='lightgoldenrodyellow', hovercolor='0.975')
    btn60.on_clicked(lambda event: buttonClick(60))

    buttonAxis75 = plt.axes([0.65, 0.05, 0.1, 0.04])
    btn75 = Button(buttonAxis75, '75', color='lightgoldenrodyellow', hovercolor='0.975')
    btn75.on_clicked(lambda event: buttonClick(75))

    buttonAxis90 = plt.axes([0.76, 0.05, 0.1, 0.04])
    btn90 = Button(buttonAxis90, '90', color='lightgoldenrodyellow', hovercolor='0.975')
    btn90.on_clicked(lambda event: buttonClick(90))

    buttonAxisFull = plt.axes([0.87, 0.05, 0.1, 0.04])
    btnFull = Button(buttonAxisFull, 'Full', color='lightgoldenrodyellow', hovercolor='0.975')
    btnFull.on_clicked(lambda event: buttonClick(120))

    plt.show()


def main():
    showPassNetwork(120)
    

if __name__ == "__main__":
    main()
