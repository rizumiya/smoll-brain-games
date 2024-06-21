import streamlit as st

from utils import hide_st, initial_db, initial_records

st.set_page_config(
    page_title="Welcome Player",
    page_icon="👋",
)
hide_st(st)

st.subheader("🧠 Brain Game - _Go Brain Go!_")

st.write(
    """
    **Welcome to a mind-bending world of puzzles!**

    In this game, you'll embark on a journey of mental challenges designed to sharpen your intellect and ignite your creativity. From enigmatic numbers to cryptic words to jumbled letters, each puzzle is a unique enigma waiting to be solved.

    With an intuitive interface and a focus on pure gameplay, this game provides an immersive experience that will keep you engaged for hours on end. So, gather your wits, embrace the challenge, and let the brain games begin!
    """.replace("    ", "")
)

initial_db()
# initial_records()
