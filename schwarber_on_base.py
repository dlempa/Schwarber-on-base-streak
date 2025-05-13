import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🔥 Kyle Schwarber On-Base Streak Tracker")

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

st.header(f" Current On-Base Streak: {streak} games")
st.write(f"Streak spans {seasons[0]} and {seasons[-1]} regular season games.")
st.write(f"Updated as of: {datetime.now().strftime('%Y-%m-%d')}")

if st.checkbox("Show game logs"):
    st.dataframe(df[['date', 'season', 'opponent', 'hits', 'walks', 'HBP', 'reached_base']].head(streak),hide_index=True)


# Step 7: Create the all-time on-base streak leaderboard (static + Schwarber live)
historical_streaks = [
{"name": "Ted Williams", "team": "BOS", "streak": 84, "seasons": "1949"},
    {"name": "Ted Williams", "team": "BOS", "streak": 74, "seasons": "1941-1942"},
    {"name": "Joe DiMaggio", "team": "NYY", "streak": 74, "seasons": "1941"},
    {"name": "Orlando Cabrera", "team": "LAA", "streak": 63, "seasons": "2006"},
    {"name": "Mark McGwire", "team": "OAK", "streak": 62, "seasons": "1995-1996"},
    {"name": "Jim Thome", "team": "CLE,PHI", "streak": 60, "seasons": "2002-2003"},
    {"name": "Will Clark", "team": "TEX", "streak": 59, "seasons": "1995-1996"},
    {"name": "Barry Bonds", "team": "SFG", "streak": 58, "seasons": "2003"},
    {"name": "Barry Bonds", "team": "SFG", "streak": 58, "seasons": "2001-2002"},
    {"name": "Duke Snider", "team": "BRO", "streak": 58, "seasons": "1954"},
    {"name": "Derek Jeter", "team": "NYY", "streak": 57, "seasons": "1998-1999"},
    {"name": "Frank Thomas", "team": "CHW", "streak": 57, "seasons": "1995-1996"},
    {"name": "Wade Boggs", "team": "BOS", "streak": 57, "seasons": "1985"},
    {"name": "George Kell", "team": "DET", "streak": 57, "seasons": "1950"},
    {"name": "Roger Bresnahan", "team": "NYG", "streak": 57, "seasons": "1904"},
    {"name": "Ryan Klesko", "team": "SDP", "streak": 56, "seasons": "2002"},
    {"name": "Mike Schmidt", "team": "PHI", "streak": 56, "seasons": "1981-1982"},
    {"name": "Arky Vaughan", "team": "PIT", "streak": 56, "seasons": "1936"},
    {"name": "Stan Musial", "team": "STL", "streak": 55, "seasons": "1943"},
    {"name": "Harry Heilmann", "team": "DET", "streak": 55, "seasons": "1922-1923"},
    {"name": "Ty Cobb", "team": "DET", "streak": 55, "seasons": "1915"},
    {"name": "Luke Appling", "team": "CHW", "streak": 54, "seasons": "1938-1939"},
    {"name": "Ray Blades", "team": "STL", "streak": 54, "seasons": "1925"},
    {"name": "Álex Rodríguez", "team": "NYY", "streak": 53, "seasons": "2004"},
    {"name": "Shawn Green", "team": "LAD", "streak": 53, "seasons": "2000"},
    {"name": "Luke Appling", "team": "CHW", "streak": 53, "seasons": "1936"},
    {"name": "Matty McIntyre", "team": "DET", "streak": 53, "seasons": "1908"},
    {"name": "Shin-Soo Choo", "team": "TEX", "streak": 52, "seasons": "2018"},
    {"name": "Kevin Millar", "team": "BAL", "streak": 52, "seasons": "2007"},
    {"name": "Gary Sheffield", "team": "ATL", "streak": 52, "seasons": "2002"},
    {"name": "Tony Phillips", "team": "DET", "streak": 52, "seasons": "1993"},
    {"name": "Greg Gross", "team": "HOU", "streak": 52, "seasons": "1975"},
    {"name": "Jim Wynn", "team": "HOU", "streak": 52, "seasons": "1969"},
    {"name": "Mel Almada", "team": "SLB,WSH", "streak": 52, "seasons": "1938"},
    {"name": "Joe DiMaggio", "team": "NYY", "streak": 52, "seasons": "1937"},
    {"name": "Lou Gehrig", "team": "NYY", "streak": 52, "seasons": "1934"},
    {"name": "Jack Tobin", "team": "SLB", "streak": 52, "seasons": "1922"},
    {"name": "Tris Speaker", "team": "CLE", "streak": 52, "seasons": "1920"},
    {"name": "Ty Cobb", "team": "DET", "streak": 52, "seasons": "1914"},
    {"name": "George Brett", "team": "KCR", "streak": 51, "seasons": "1980"},
    {"name": "Ben Chapman", "team": "NYY", "streak": 51, "seasons": "1933"},
    {"name": "Ken Williams", "team": "SLB", "streak": 51, "seasons": "1923"},
    {"name": "Babe Ruth", "team": "NYY", "streak": 51, "seasons": "1923"},
    {"name": "Lou Whitaker", "team": "DET", "streak": 50, "seasons": "1991"},
    {"name": "Vince Coleman", "team": "STL", "streak": 50, "seasons": "1987"},
    {"name": "Joe Vosmik", "team": "BOS", "streak": 50, "seasons": "1938"},
    {"name": "Paul Waner", "team": "PIT", "streak": 50, "seasons": "1936-1937"},
    {"name": "Tris Speaker", "team": "CLE", "streak": 50, "seasons": "1926"},
    {"name": "Johnny Bates", "team": "CIN", "streak": 50, "seasons": "1911"},
    {"name": "Manny Ramírez", "team": "CLE", "streak": 49, "seasons": "2000"},
    {"name": "Phil Nevin", "team": "SDP", "streak": 49, "seasons": "2000"},
    {"name": "Ken Singleton", "team": "BAL", "streak": 49, "seasons": "1977"},
    {"name": "Jimmie Foxx", "team": "BOS", "streak": 49, "seasons": "1939"},
    {"name": "Lou Gehrig", "team": "NYY", "streak": 49, "seasons": "1935"},
    {"name": "Lou Gehrig", "team": "NYY", "streak": 49, "seasons": "1933-1934"},
    {"name": "Chuck Klein", "team": "PHI", "streak": 49, "seasons": "1930"},
    {"name": "Harry Heilmann", "team": "DET", "streak": 49, "seasons": "1923-1924"},
    {"name": "Tommy Pham", "team": "TBR", "streak": 48, "seasons": "2018-2019"},
    {"name": "Joey Votto", "team": "CIN", "streak": 48, "seasons": "2015"},
    {"name": "Albert Pujols", "team": "STL", "streak": 48, "seasons": "2001"},
    {"name": "Bobby Abreu", "team": "PHI", "streak": 48, "seasons": "2000-2001"},
    {"name": "Jim Thome", "team": "CLE", "streak": 48, "seasons": "1999"},
    {"name": "Tony Phillips", "team": "DET", "streak": 48, "seasons": "1993"},
    {"name": "Dale Murphy", "team": "ATL", "streak": 48, "seasons": "1987"},
    {"name": "Pete Rose", "team": "CIN", "streak": 48, "seasons": "1978"},
    {"name": "Solly Hemus", "team": "STL", "streak": 48, "seasons": "1953"},
    {"name": "Ted Williams", "team": "BOS", "streak": 48, "seasons": "1951"},
    {"name": "Ted Williams", "team": "BOS", "streak": 48, "seasons": "1942-1946"},
    {"name": "Ray Sanders", "team": "STL", "streak": 48, "seasons": "1944"},
    {"name": "Stan Spence", "team": "WSH", "streak": 48, "seasons": "1942"},
    {"name": "Marv Owen", "team": "CHW", "streak": 48, "seasons": "1938"},
    {"name": "Zeke Bonura", "team": "CHW", "streak": 48, "seasons": "1936"},
    {"name": "Eddie Collins", "team": "CHW", "streak": 48, "seasons": "1917-1918"},
    {"name": "Kyle Schwarber", "team": "PHI", "streak": streak, "seasons": "2024-2025"},
    {"name": "Matt Holliday", "team": "STL", "streak": 47, "seasons": "2014-2015"},
]

df_streaks = pd.DataFrame(historical_streaks)
df_streaks = df_streaks[df_streaks['streak'] > 0]
df_streaks = df_streaks.sort_values(by='streak', ascending=False).reset_index(drop=True)
df_streaks['Rank'] = df_streaks.index + 1



# Highlight Schwarber’s row
def highlight_schwarber(row):
    return ['background-color: yellow' if row['name'] == 'Kyle Schwarber' else '' for _ in row]



styled_df= (
    df_streaks[['Rank', 'name', 'streak', 'seasons']]
    .reset_index(drop=True)
    .style
    .apply(highlight_schwarber, axis=1)
    .set_properties(**{'text-align': 'center'})
)


schwarber_row = df_streaks[df_streaks['name']=='Kyle Schwarber']
schwarber_rank = schwarber_row.index[0] + 1

st.subheader("All-Time On-Base Streaks")
st.write(f"Schwarber currently ranks number {schwarber_rank} all-time in consecutive regular season games reaching base safely.")
st.dataframe(styled_df, use_container_width=True,hide_index=True)



st.markdown("""
---
**Data Disclaimer**:  
This app uses data sourced from the **unofficial MLB Stats API**. Data accuracy and availability depend entirely on MLB's API and are not guaranteed. MLB holds all rights to the underlying data.
""")
