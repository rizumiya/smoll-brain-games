import streamlit as st

from utils import *


st.set_page_config(
    page_title="Leaderboards",
    page_icon="🏆",
    layout="centered"
)
hide_st(st)


st.info("Under Construction", icon="🚧")

rows = get_leaderboard()

data_histories = []
for row in rows:
    data_histories.append({
        "player_name": row[0],
        "skor": row[1],
        "game_date": row[2]
    })

# Menampilkan data dalam bentuk tabel
edited_df = st.data_editor(
    data_histories,
    height=300,
    column_order=['game_date', 'player_name', 'skor'],
    column_config={
        "game_date": st.column_config.TextColumn("Date", disabled=True),
        "player_name": st.column_config.TextColumn("Name", disabled=True),
        "skor": st.column_config.NumberColumn("Your Skor", disabled=True)
    },
    num_rows="fixed",
    use_container_width=True,
    hide_index=True
)

