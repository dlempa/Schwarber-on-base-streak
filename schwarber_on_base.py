import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🔥 Kyle Schwarber's Multi-Season On-Base Streak Tracker")

player_id = 656941
seasons = [2024, 2025]

@st.cache_data(show_spinner=True)
def get_game_logs(player_id, seasons):
    logs = []
    for season in seasons:
        url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats"
        params = {
            "stats": "gameLog",
            "season": season,
            "group": "hitting",
            "gameType": "R"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if 'stats' in data and data['stats'] and 'splits' in data['stats'][0]:
            logs.extend(data['stats'][0]['splits'])
        else:
            st.warning(f"No game log data available yet for the {season} season.")
            
    return logs

game_logs = get_game_logs(player_id, seasons)

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
df['reached_base'] = (df['hits'] + df['walks'] + df['HBP']) > 0
df = df.sort_values(by='date', ascending=False).reset_index(drop=True)

streak = 0
for reached in df['reached_base']:
    if reached:
        streak += 1
    else:
        break

st.header(f"📅 Current On-Base Streak: {streak} games")
st.write(f"Streak spans {seasons[0]} and {seasons[-1]} seasons.")
st.write(f"Updated as of: {datetime.now().strftime('%Y-%m-%d')}")

if st.checkbox("Show recent game logs"):
    st.dataframe(df[['date', 'season', 'opponent', 'hits', 'walks', 'HBP', 'reached_base']].head(15))

st.markdown("""
---
⚠️ **Data Disclaimer**:  
This app uses data sourced from the **unofficial MLB Stats API**. Data accuracy and availability depend entirely on MLB's API and are not guaranteed. MLB holds all rights to the underlying data.
""")
