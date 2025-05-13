import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🔥 Kyle Schwarber's Multi-Season On-Base Streak Tracker")

# Kyle Schwarber's Player ID
player_id = 656941
seasons = [2024, 2025]  # Seasons to include

# Function to fetch game logs for multiple seasons
@st.cache_data(show_spinner=True)
def get_game_logs(player_id, seasons):
    logs = []
    for season in seasons:
        url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats/game"
        params = {
            "season": season,
            "group": "hitting",
            "gameType": "R"
        }
        response = requests.get(url, params=params)
        data = response.json()
        logs.extend(data['stats'][0]['splits'])
    return logs

# Fetch logs for both seasons
game_logs = get_game_logs(player_id, seasons)

# Build combined DataFrame
logs = []
for game in game_logs:
    stats = game['stat']
    logs.append({
        'date': game['date'],
        'season': game['season'],
        'opponent': game['opponent']['name'],
        'hits': int(stats['hits']),
        'walks': int(stats['baseOnBalls']),
        'HBP': int(stats['hitByPitch']),
        'PA': int(stats['plateAppearances']),
    })

df = pd.DataFrame(logs)

# Check if Schwarber reached base safely in each game
df['reached_base'] = (df['hits'] + df['walks'] + df['HBP']) > 0

# Sort games chronologically from most recent
df = df.sort_values(by='date', ascending=False).reset_index(drop=True)

# Calculate current streak spanning multiple seasons
streak = 0
for reached in df['reached_base']:
    if reached:
        streak += 1
    else:
        break

# Display results
st.header(f"📅 Current On-Base Streak: {streak} games")
st.write(f"Streak spans {seasons[0]} and {seasons[-1]} seasons.")
st.write(f"Updated as of: {datetime.now().strftime('%Y-%m-%d')}")

# show recent games across seasons
if st.checkbox("Show recent game logs"):
    st.dataframe(df[['date', 'season', 'opponent', 'hits', 'walks', 'HBP', 'reached_base']].head(15))

st.markdown("""
---
⚠️ **Data Disclaimer**:  
This app uses data sourced from the **unofficial MLB Stats API**. It is provided for informational and educational purposes only. Data availability, accuracy, and timeliness depend entirely on MLB's API and are not guaranteed. MLB holds all rights to the underlying data.
""")
