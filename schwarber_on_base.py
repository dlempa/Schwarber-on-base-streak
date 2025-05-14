# app.py
import streamlit as st
import requests
import pandas as pd
import json
import os
from datetime import datetime, timedelta

st.title("🔥 Kyle Schwarber On-Base Streak Tracker")

player_id = 656941
seasons = [2024, 2025]
STREAK_FILE = "schwarber_streak.json"

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

def load_streak():
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, 'r') as f:
            return json.load(f)
    return {
        "status": "active",
        "streak": 0,
        "start_date": None,
        "end_date": None,
        "games": [],
        "final_rank": None
    }

def save_streak(data):
    with open(STREAK_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def is_game_final(game_pk):
    try:
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
        data = requests.get(url).json()
        return data['gameData']['status'].get('codedGameState', '') == 'F'
    except Exception as e:
        st.warning(f"Could not check game status for gamePk {game_pk}: {e}")
        return False

# Load logs and filter incomplete games
game_logs = get_game_logs(player_id, seasons)
logs = []

@st.cache_data(show_spinner=True)
def build_logs(game_logs):
    logs = []
    for i, game in enumerate(game_logs):
        game_pk = game['game']['gamePk']
        game_date = game['date']

        # Skip only the first game (most recent) if it's not final
        if i == 0 and not is_game_final(game_pk):
            st.info(f"Game on {game_date} (gamePk {game_pk}) is still in progress and was excluded.")
            continue

        stats = game['stat']
        logs.append({
            'gamePk': game_pk,
            'date': game_date,
            'season': game['season'],
            'opponent': game['opponent']['name'],
            'hits': int(stats['hits']),
            'walks': int(stats['baseOnBalls']),
            'HBP': int(stats['hitByPitch']),
            'PA': int(stats['plateAppearances']),
        })

    return logs


logs = build_logs(game_logs)
df = pd.DataFrame(logs)
df['reached_base'] = (df['hits'] + df['walks'] + df['HBP']) > 0
df = df.sort_values(by='date', ascending=False).reset_index(drop=True)

# Calculate streak
current_streak = 0
for reached in df['reached_base']:
    if reached:
        current_streak += 1
    else:
        break

saved_data = load_streak()

if saved_data["status"] == "active" and current_streak < saved_data["streak"] and current_streak != 0:
    saved_data.update({
        "status": "ended",
        "end_date": df.iloc[0]["date"],
        "games": df.head(saved_data["streak"]).to_dict(orient='records')
    })
    save_streak(saved_data)

if current_streak > saved_data["streak"]:
    saved_data.update({
        "status": "active",
        "streak": current_streak,
        "start_date": df.iloc[current_streak - 1]["date"],
        "end_date": None,
        "games": df.head(current_streak).to_dict(orient='records'),
        "final_rank": None
    })
    save_streak(saved_data)

# Display current streak
if saved_data['status'] == "active":
    st.header(f" Current On-Base Streak: {saved_data['streak']} games")
    st.write(f"Streak spans {seasons[0]} and {seasons[-1]} regular season games.")
    st.write(f"Updated as of: {datetime.now().strftime('%Y-%m-%d')}")
    if st.checkbox("Show game logs"):
        st.dataframe(df[['date', 'season', 'opponent', 'hits', 'walks', 'HBP', 'reached_base']].head(saved_data['streak']), hide_index=True)

# Load historical streaks from CSV
df_historical = pd.read_csv("historical_streaks.csv")

# Remove existing Schwarber row if present
df_historical = df_historical[df_historical['name'] != 'Kyle Schwarber']

# Add current Schwarber streak
if saved_data["status"] == "active":
    df_historical = pd.concat([df_historical, pd.DataFrame([{
        "name": "Kyle Schwarber",
        "team": "PHI",
        "streak": saved_data["streak"],
        "seasons": "2024–2025"
    }])], ignore_index=True)

elif saved_data["status"] == "ended":
    df_historical = pd.concat([df_historical, pd.DataFrame([{
        "name": "Kyle Schwarber",
        "team": "PHI",
        "streak": saved_data["streak"],
        "seasons": f"{saved_data['start_date']} to {saved_data['end_date']}"
    }])], ignore_index=True)


# Build streak leaderboard
df_streaks = df_historical[df_historical['streak'] > 0].copy()
df_streaks = df_streaks.sort_values(by='streak', ascending=False).reset_index(drop=True)
df_streaks['Rank'] = df_streaks.index + 1

if saved_data["status"] == "ended" and saved_data["final_rank"] is None:
    schwarber_row = df_streaks[df_streaks['name'] == 'Kyle Schwarber']
    if not schwarber_row.empty:
        saved_data["final_rank"] = schwarber_row.index[0] + 1
        save_streak(saved_data)

# Display leaderboard
st.subheader("All-Time On-Base Streaks")
if saved_data["status"] == "ended":
    st.write(f"⚠️ Kyle Schwarber's streak ended at **{saved_data['streak']} games**, ranked **#{saved_data['final_rank']} all-time**.")
    if st.checkbox("Show ended streak game logs"):
        st.dataframe(pd.DataFrame(saved_data["games"]), hide_index=True)
else:
    schwarber_row = df_streaks[df_streaks['name'] == 'Kyle Schwarber']
    if not schwarber_row.empty:
        schwarber_rank = schwarber_row.index[0] + 1
        st.write(f"Schwarber currently ranks number {schwarber_rank} all-time in consecutive games reaching base safely.")

st.dataframe(
    df_streaks.style
    .apply(lambda row: ['background-color: yellow' if row['name'] == 'Kyle Schwarber' else '' for _ in row], axis=1)
    .set_properties(**{'text-align': 'center'}),
    use_container_width=True,
    hide_index=True
)

st.markdown("""
---
**Data Disclaimer**:  
This app uses data sourced from the **unofficial MLB Stats API**. Data accuracy and availability depend entirely on MLB's API and are not guaranteed. MLB holds all rights to the underlying data.
""")
